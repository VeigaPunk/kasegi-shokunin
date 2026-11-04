PASS — C1 named probe-set predicate reproduced at the implementation pin; no actionable in-scope defect.

## Scope and axes
Axes: depth:verifiability (C1); coverage limited to its named probes and controls. Recommendation only, not admission. No C2 checks, extra attack probes, suite, delegation, installation, production edits, or commits performed. This is not a sandbox verdict or a universal shell-path claim.

## Identity and setup receipts
Lane: /home/vgpnk/Projects/shokunin/kasegi-shokunin
Clone (removed after checks): /fast/scratch/hyaku/kasegi-r61/ReviewC1/clone
Every probe process used cwd=/fast/scratch/hyaku/kasegi-r61/ReviewC1/clone, TMPDIR=/fast/scratch/hyaku/kasegi-r61/ReviewC1, PYTHONDONTWRITEBYTECODE=1. Children inherited the same TMPDIR. Commands below use absolute entry paths; derives internal to the committed fixture retain their required relative paths.

Setup commands (exit 0 each):
```sh
mkdir -p /fast/scratch/hyaku/kasegi-r61/ReviewC1
git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin rev-parse HEAD
# 13c8060b343e002339ffd72da37ff74514f82765
git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin show 6f88f3a7f6b9689b49241e3f4a8e551c57a3f766:.ufo/waves/round-61/claims.json
git -C /fast/scratch/hyaku/kasegi-r61/ReviewC1 clone --shared --no-checkout /home/vgpnk/Projects/shokunin/kasegi-shokunin /fast/scratch/hyaku/kasegi-r61/ReviewC1/clone
git -C /fast/scratch/hyaku/kasegi-r61/ReviewC1/clone rev-parse --show-toplevel
# /fast/scratch/hyaku/kasegi-r61/ReviewC1/clone — asserted before checkout
git -C /fast/scratch/hyaku/kasegi-r61/ReviewC1/clone checkout --detach 13c8060b343e002339ffd72da37ff74514f82765
git -C /fast/scratch/hyaku/kasegi-r61/ReviewC1/clone diff c33d24ddd11abf1ebdea0dccf7327e9069dd9104 13c8060b343e002339ffd72da37ff74514f82765 -- corpus/instruments/figure-audit.py corpus/instruments/figure-audit-mutbat.py .ufo/waves/round-61/controls/c1-probe-run-r61.sh
```
Frozen claims JSON loaded from git-show output equaled the working claims JSON. Both frozen C1 digests matched the pinned clone, computed with Python hashlib.sha256(Path.read_bytes()).hexdigest():
- corpus/instruments/figure-audit.py: 051083a2dd3b76f96568dd2a18866975b71dd1578992546c671faf21e99418a9
- corpus/instruments/figure-audit-mutbat.py: f94393d981eeb93a05f6c57782b787faabfc56bfa5b4775f1c319f405fdd353c

## Exact counting commands and complete outputs
The five assigned checks ran concurrently, each once. The runner scratch argument was changed only from the shared verify/probes path to this seat's distinct scratch. Outer runner exit alone is not an assertion: individual probe outputs below were checked against the frozen predicate.

```sh
bash /fast/scratch/hyaku/kasegi-r61/ReviewC1/clone/.ufo/waves/round-61/controls/c1-probe-run-r61.sh /fast/scratch/hyaku/kasegi-r61/ReviewC1/clone/corpus/instruments/figure-audit.py /fast/scratch/hyaku/kasegi-r61/ReviewC1/probes
```
```text
instrument=/fast/scratch/hyaku/kasegi-r61/ReviewC1/clone/corpus/instruments/figure-audit.py sha256=051083a2dd3b76f9
run-utc=2026-11-04T14:26:00Z
probe=P1-traversal-2up derive=python3 corpus/instruments/../../outside-P1-traversal-2up.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P1-traversal-2up
probe=P2-traversal-3up derive=python3 corpus/instruments/../../../outside-P2-traversal-3up.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P2-traversal-3up
probe=P3-symlink-out derive=python3 corpus/instruments/link-P3-symlink-out.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P3-symlink-out
probe=P4-absolute-out derive=python3 /fast/scratch/hyaku/kasegi-r61/ReviewC1/probes/outside-P4-absolute-out.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P4-absolute-out
probe=P5-inside-ok derive=python3 corpus/instruments/tiny-ok.py exit=0 markers=0 :: FIG P5-inside-ok recorded=35 derived=35 ok
probe=P6-inside-normalized derive=python3 corpus/instruments/../instruments/tiny-ok.py exit=0 markers=0 :: FIG P6-inside-normalized recorded=35 derived=35 ok
probe=CTRL-quoted-semicolon derive=cat g.txt | grep -e '35' -e ';' exit=0 markers=0 :: FIG CTRL-quoted-semicolon recorded=35 derived=35 ok
probe=CTRL-plain-count derive=cat g.txt | wc -l exit=0 markers=0 :: FIG CTRL-plain-count recorded=1 derived=1 ok
EXIT=0
```

```sh
python3 /fast/scratch/hyaku/kasegi-r61/ReviewC1/clone/corpus/instruments/figure-audit.py --selftest
```
```text
selftest case=ok-ledger exit=0 want=0 verdict=pass
selftest case=stale-literal exit=1 want=1 verdict=pass
selftest case=derive-fails-fail-closed exit=1 want=1 verdict=pass
selftest case=token-boundary-34-vs-340 exit=1 want=1 verdict=pass
selftest case=unreadable-ledger-exit-2 exit=2 want=2 verdict=pass
selftest case=derive-not-read-only-refused exit=2 want=2 verdict=pass
selftest case=chain-semicolon-refused exit=2 want=2 verdict=pass
selftest case=chain-background-refused exit=2 want=2 verdict=pass
selftest case=chain-newline-refused exit=2 want=2 verdict=pass
selftest case=chain-cmdsubst-refused exit=2 want=2 verdict=pass
selftest case=pipe-to-shell-refused exit=2 want=2 verdict=pass
selftest case=redirect-refused exit=2 want=2 verdict=pass
selftest case=or-chain-refused exit=2 want=2 verdict=pass
selftest case=quoted-separator-admitted exit=0 want=0 verdict=pass
selftest case=escape-single-quote-refused exit=2 want=2 verdict=pass
selftest case=escape-double-quote-refused exit=2 want=2 verdict=pass
selftest case=sed-head-refused exit=2 want=2 verdict=pass
selftest case=awk-head-refused exit=2 want=2 verdict=pass
selftest case=sort-output-flag-refused exit=2 want=2 verdict=pass
selftest case=git-show-output-flag-refused exit=2 want=2 verdict=pass
selftest case=python-inside-admitted exit=0 want=0 verdict=pass
selftest case=python-traversal-refused exit=2 want=2 verdict=pass
selftest case=python-symlink-refused exit=2 want=2 verdict=pass
selftest case=python-absolute-refused exit=2 want=2 verdict=pass
selftest cases=24 failures=0
EXIT=0
```

```sh
python3 /fast/scratch/hyaku/kasegi-r61/ReviewC1/clone/corpus/instruments/figure-audit-mutbat.py
```
```text
PRISTINE selftest_exit=0 last='selftest cases=24 failures=0'
CONTROL c-equivalent-trailing-space selftest_exit=0 must_not_be_killed=held last='selftest cases=24 failures=0'
MUT m4-drop-stale-literal-case sites=1 py_compile=0 selftest_exit=1 killed=1 last='selftest cases=23 failures=1'
MUT m6-readonly-gate-off sites=1 py_compile=0 selftest_exit=1 killed=1 last='selftest cases=24 failures=4'
MUT m7-python-confinement-off sites=1 py_compile=0 selftest_exit=1 killed=1 last='selftest cases=24 failures=2'
mutbat killed=3/3 survivors=0 controls=pass
EXIT=0
```

```sh
python3 /fast/scratch/hyaku/kasegi-r61/ReviewC1/clone/corpus/instruments/figure-audit.py
```
```text
FIG frontier-rows recorded=34 derived=34 ok
FIG registry-rows recorded=85 derived=85 ok
FIG knowledge-expected-entries recorded=72 derived=72 ok
FIG knowledge-files recorded=72 derived=72 ok
FIG capture-lines-s085 recorded=543 (filed; superseded by the r54 D53-2 correction) derived=542 ok
FIG capture-bytes-s085 recorded=7590 derived=7590 ok
FIG capture-lines-s086 recorded=731 derived=731 ok
FIG capture-sha256-s086 recorded=fa84a01753971589571c22597d5b7f65ed34dc373dfc466d2233437faf4dc81f derived=fa84a01753971589571c22597d5b7f65ed34dc373dfc466d2233437faf4dc81f ok
FIG frontier-rows-r54 recorded=35 derived=35 ok
FIG registry-rows-r54 recorded=86 derived=86 ok
FIG entries-r54 recorded=38 derived=38 ok
FIG knowledge-expected-r54 recorded=73 derived=73 ok
FIG knowledge-files-r54 recorded=73 derived=73 ok
FIG figure-audit-mentions-base-scorecard recorded=2 (the receipt's limb; the filed prose 0 superseded) derived=2 ok
FIG figure-audit-mentions-base-log recorded=0 derived=0 ok
FIG figure-audit-mentions-base-knowledge-expected recorded=0 derived=0 ok
FIG frontier-rows-r55 recorded=36 derived=36 ok
FIG registry-rows-r55 recorded=87 derived=87 ok
FIG entries-r55 recorded=39 derived=39 ok
FIG knowledge-expected-r55 recorded=74 derived=74 ok
FIG knowledge-files-r55 recorded=74 derived=74 ok
FIG census-fresh-literal-r55 recorded=stale (the receipt's printed limb; the filed prose ok superseded) derived=stale ok
FIG census-internal-r55-receipt recorded=1118 derived=1118 ok
FIG census-gone-r55-receipt recorded=3883 derived=3883 ok
FIG census-fixedpoint-internal-r55 recorded=1119 derived=1119 ok
FIG census-fixedpoint-gone-r55 recorded=3882 derived=3882 ok
FIG fail-entry-records recorded=33 (the class-check line; the trailer's 34 superseded) derived=33 ok
FIG frontier-rows-r56 recorded=37 derived=37 ok
FIG registry-rows-r56 recorded=88 derived=88 ok
FIG entries-r56 recorded=40 derived=40 ok
FIG knowledge-expected-r56 recorded=75 derived=75 ok
FIG knowledge-files-r56 recorded=75 derived=75 ok
FIG census-fresh-literal-r56 recorded=ok derived=ok ok
FIG census-internal-r56-receipt recorded=1130 derived=1130 ok
FIG census-gone-r56-receipt recorded=3915 derived=3915 ok
FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0
EXIT=0
```

```sh
python3 /fast/scratch/hyaku/kasegi-r61/ReviewC1/clone/corpus/instruments/figure-audit.py --ledger /fast/scratch/hyaku/kasegi-r61/ReviewC1/clone/.ufo/waves/round-54/controls/red-d53-ledger.json
```
```text
FIG d53-1-trailer recorded=34 derived=33 want=34 stale
FIG d53-2-lines recorded=543 derived=542 want=543 stale
FIGURE-AUDIT figures=2 ok=0 stale=2 exit=1
EXIT=1
```

## Changed behavior and path:line evidence
All evidence paths below refer to the immutable implementation pin; each can be prefixed with /home/vgpnk/Projects/shokunin/kasegi-shokunin/.
- .ufo/waves/round-61/claims.json:13-32 fixes the predicate, five commands, expected digests and residuals; no counting rule was amended.
- corpus/instruments/figure-audit.py:172-187 resolves the candidate and instruments base with realpath, rejects the base itself, then requires the base-plus-separator prefix. This handles the named two-up, three-up and out-pointing symlink probes without rejecting the normalized inside path.
- corpus/instruments/figure-audit.py:190-203 threads root through segment_ok and check_read_only; :225-228 passes audit's root and returns exit 2 before run_derive on refusal. run_derive uses the same root as cwd (:72-87). This is the canonical gate/execution logic, not merely a restatement of expected results.
- .ufo/waves/round-61/controls/c1-probe-run-r61.sh:23-38 creates separate roots, captures real instrument exits and counts MARK files; :41-54 defines all eight named probes/controls. P1-P4 each actually showed exit 2, markers 0 and derive-not-read-only; all four admitted controls showed the required derived values.
- corpus/instruments/figure-audit.py:286-295 constructs inside/outside/symlink fixtures; :333-336 adds the four cases. :303-309 executes the real instrument; :338-347 pins the case count. Observed tally: 24/0.
- corpus/instruments/figure-audit-mutbat.py:23-34 defines three mutants and the equivalent control; :50-67 checks pristine and equivalent controls; :69-97 validates exact-once mutation, syntax compilation and selftest rejection. All three compiled and were killed; pristine and equivalent controls passed. This is 3/3 of this battery only, not mutation saturation.
- corpus/instruments/figure-audit.py:229-241 classifies nonzero/empty derivations and comparisons as stale and emits the observed aggregate exit. Ledger 35/35 and both red rows stale agree with their receipts above.

## Findings by severity
None within the frozen C1 predicate. All named acceptance checks matched, including expected red-fixture exit 1.

## Residual risks and verification gaps
- Retained design limitation: raw head.split()/realpath (:180-184) is not a shell decoder, while execution remains bash -c (:77). Expansion/quoting semantics are expressly outside this predicate; no broader confinement conclusion drawn.
- Retained design limitation: other allow-listed heads and the contents of allowed Python counters are not sandboxed (:190-195, :77). No extra attack probes were run, and no residual was reclassified as a C1 failure.
- Host-conditional evidence: selftest invokes the host `python` command (:305), so 24/0 is an observation on this host, not portability proof. Symlink setup catches failures (:291-295), which is another reason not to extrapolate the tally across hosts.
- LSP device unavailable: reading xd://lsp returned “No such tool”. Semantic references/definition/diagnostics could not be obtained. Fallback textual reference search found the changed function definitions and their updated production calls in figure-audit.py; historical wave receipts retain old signatures as data. This search is not semantic proof. No runtime routing/resume changes occur in the scoped diff.
- Full diff inspection was limited to C1's two instrument files and committed probe runner; C2 is deliberately outside this seat.

## Cleanup and tools
No tools installed or updated. Cleanup command (exit 0):
```sh
rm -rf -- /fast/scratch/hyaku/kasegi-r61/ReviewC1 && test ! -e /fast/scratch/hyaku/kasegi-r61/ReviewC1
```
Complete command outputs are preserved inline above; no scratch receipts remain. Only this report was written in the lane.

Self-evaluation: accuracy 4 (runtime receipts and hashes; no LSP semantic evidence), completeness 5 (all five assigned checks and digests), clarity 4 (full receipts are long), actionability 5 (exact commands and source anchors), conciseness 4 (full output retained for verifiability); mean 4.4/5. Scope was not broadened to improve a score.
