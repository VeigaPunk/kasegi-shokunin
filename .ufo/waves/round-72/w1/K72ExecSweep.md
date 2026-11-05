# K72ExecSweep — measured regression sweep

Axes: admission parity, refusal direction, realpath boundary coverage, retained evidence.

## Setup and pinned bytes
`S=/fast/scratch/hyaku/kasegi-r72/K72ExecSweep`
`git clone --shared --no-checkout /home/vgpnk/Projects/shokunin/kasegi-shokunin "$S/lane"` returned rc=0.
`git archive a34ce4c` was extracted with Python tarfile into the clone (regular files/directories only).
Initial data-filter extraction rejected an absolute historical symlink; resumed extraction omitted symlinks. No checkout, add, commit, reset, or source-tree mutation.
`git -C "$S/lane" rev-parse HEAD` printed `a34ce4c146b669ea8038da32ba47d7ca3b36ea43`.
Candidate gate copied byte-for-byte from the supplied working-tree file; base gate obtained with `git show a34ce4c:corpus/instruments/figure-audit.py`.
SHA256 (hashlib over copied bytes):
```
base-figure-audit.py 182f4ef7d9c9e4d921482d1c2d0cde113c49fd40c76f8fdf0319ba86ba064603
figure-audit.py b146c81a29437aef2d4e91576782a2829570ac12f13888cad099d6081d1fefdc
derive-head-census.py 255fd4072dfe8e2a6bf53d5fcc0f92d2af486d40711d03c4573a4017ccd8db52
```

## Collection
Literal `python3 corpus/instruments` search used the specialized grep tool (equivalent to requested grep -n). Repeated committed receipt commands were deduplicated; N1–N12 and R1–R8 were AST-evaluated from their list expressions (no probe-driver execution).
The committed figure-audit-ledger.json contained 35 figures and 0 python derives.
The probe controls C0/C1 used a scratch-only `corpus/instruments/ok.py` containing `print(35)`.
Literal committed hits:
```
attempt2-tip-counters.txt:37:# command: python3 corpus/instruments/frontier-recheck-count.py | head -2
attempt2-tip-counters.txt:41:# command: python3 corpus/instruments/capture-binding-check.py | tail -1
attempt2-tip-counters.txt:66:# command: python3 corpus/instruments/frontier-recheck-count.py | head -2
attempt2-tip-counters.txt:71:# command: python3 corpus/instruments/capture-binding-check.py | tail -1
c1-forgery-r71.txt:23:MEASURE read-only-controls-admitted FAIL controls=8 failed=8 python3 corpus/instruments/ok.py rc=2;python3 corpus/instruments/ok.py -- --root rc=2;cat g.txt rc=2;grep -c 35 g.txt rc=2;sort g.txt | head -n 1 rc=2;cut -c1-2 g.txt | head -n 1 rc=2;git show HEAD:g.txt | head -n 1 rc=2;git cat-file -t HEAD rc=2
c1-probe-run-r71.py:237:         "python3 corpus/instruments/capture-binding-check.py --selftest", None),
c1-probe-run-r71.py:244:        ("N12-python-unknown-head", "python3 corpus/instruments/r99-unknown-probe.py", None),
c1-probe-run-r71.py:257:        ("R1-capture-binding-root", "python3 corpus/instruments/capture-binding-check.py --root ."),
c1-probe-run-r71.py:258:        ("R2-kill-rule-root", "python3 corpus/instruments/kill-rule-check.py --root ."),
c1-probe-run-r71.py:259:        ("R3-frontier-count-root", "python3 corpus/instruments/r44-frontier-count.py --root ."),
c1-probe-run-r71.py:261:         "python3 corpus/instruments/claim-package-check.py "
c1-probe-run-r71.py:263:        ("R5-citation-ground-root", "python3 corpus/instruments/citation-ground-check.py --root ."),
c1-probe-run-r71.py:264:        ("R6-gate-quote-audit-root", "python3 corpus/instruments/gate-quote-audit.py --root ."),
c1-probe-run-r71.py:265:        ("R7-routed-defects-root", "python3 corpus/instruments/r44-routed-defects.py --root ."),
c1-probe-run-r71.py:267:         "python3 corpus/instruments/capture-binding-check.py --root . | grep -c records=84"),
c1-probe-run-r71.py:285:        ("python3 corpus/instruments/ok.py", fixture, "35"),
c1-probe-run-r71.py:286:        ("python3 corpus/instruments/ok.py -- --root", fixture, "35"),
```

## Execution protocol
Each row generated its own one-figure ledger (same scratch pathname overwritten between rows), with id=row-id, record=probe:1, recorded=0, derive=the exact string below, want=0.
Both actual commands per row:
```
python3 -B "$S/base-figure-audit.py" --ledger "$S/one-figure.json" --root "$S/lane"
python3 -B "$S/lane/corpus/instruments/figure-audit.py" --ledger "$S/one-figure.json" --root "$S/lane"
```
Both subprocesses used cwd=$S/lane, TMPDIR=$S, HYAKU_SCRATCH=$S, PYTHONDONTWRITEBYTECODE=1; capture_output=True, timeout=120.
A refusal means rc=2 AND stderr contains reason=derive-not-read-only. Admitted does NOT mean value-correct: want=0 intentionally makes ordinary nonzero/mismatching results stale (rc=1). No direct counter success or fixture value parity is claimed.
No URLs were fetched; N4/N5/N6/N10/N11 local file URLs were refused before execution.

## Verdict table
| Row | Exact derive string | Base verdict / rc | Candidate verdict / rc |
|---|---|---|---|
| N1-python-root-space | `python3 corpus/instruments/frontier-recheck-count.py --root .` | refused / 2 | refused / 2 |
| N2-python-root-equals | `python3 corpus/instruments/frontier-recheck-count.py --root=.` | refused / 2 | refused / 2 |
| N3-python-root-abbrev | `python3 corpus/instruments/frontier-recheck-count.py --ro .` | refused / 2 | refused / 2 |
| N4-python-out-space | `python3 corpus/instruments/capture-source.py --id x --url file:///fast/scratch/hyaku/kasegi-r72/K72ExecSweep/src.txt --out /fast/scratch/hyaku/kasegi-r72/K72ExecSweep/n4.txt --kind text` | refused / 2 | refused / 2 |
| N5-python-out-equals | `python3 corpus/instruments/capture-source.py --id x --url file:///fast/scratch/hyaku/kasegi-r72/K72ExecSweep/src.txt --out=/fast/scratch/hyaku/kasegi-r72/K72ExecSweep/n5.txt --kind text` | refused / 2 | refused / 2 |
| N6-python-out-abbrev | `python3 corpus/instruments/capture-source.py --id x --url file:///fast/scratch/hyaku/kasegi-r72/K72ExecSweep/src.txt --ou /fast/scratch/hyaku/kasegi-r72/K72ExecSweep/n6.txt --kind text` | refused / 2 | refused / 2 |
| N7-python-json-space | `python3 corpus/instruments/frontier-recheck-count.py --json /fast/scratch/hyaku/kasegi-r72/K72ExecSweep/n7.json` | refused / 2 | refused / 2 |
| N8-python-no-option-head | `python3 corpus/instruments/frontier-recheck-count.py` | refused / 2 | refused / 2 |
| N9-python-selftest | `python3 corpus/instruments/capture-binding-check.py --selftest` | refused / 2 | refused / 2 |
| N10-python-short-o | `python3 corpus/instruments/capture-source.py --id x --url file:///fast/scratch/hyaku/kasegi-r72/K72ExecSweep/src.txt -o /fast/scratch/hyaku/kasegi-r72/K72ExecSweep/n10.txt --kind text` | refused / 2 | refused / 2 |
| N11-python-output-long | `python3 corpus/instruments/capture-source.py --id x --url file:///fast/scratch/hyaku/kasegi-r72/K72ExecSweep/src.txt --output /fast/scratch/hyaku/kasegi-r72/K72ExecSweep/n11.txt --kind text` | refused / 2 | refused / 2 |
| N12-python-unknown-head | `python3 corpus/instruments/r99-unknown-probe.py` | refused / 2 | refused / 2 |
| R1-capture-binding-root | `python3 corpus/instruments/capture-binding-check.py --root .` | admitted / 1 | admitted / 1 |
| R2-kill-rule-root | `python3 corpus/instruments/kill-rule-check.py --root .` | admitted / 1 | admitted / 1 |
| R3-frontier-count-root | `python3 corpus/instruments/r44-frontier-count.py --root .` | admitted / 1 | admitted / 1 |
| R4-claim-package-json | `python3 corpus/instruments/claim-package-check.py corpus/instruments/fixtures/claim-package/exemplar --json` | admitted / 1 | admitted / 1 |
| R5-citation-ground-root | `python3 corpus/instruments/citation-ground-check.py --root .` | admitted / 1 | admitted / 1 |
| R6-gate-quote-audit-root | `python3 corpus/instruments/gate-quote-audit.py --root .` | admitted / 1 | admitted / 1 |
| R7-routed-defects-root | `python3 corpus/instruments/r44-routed-defects.py --root .` | admitted / 1 | admitted / 1 |
| R8-capture-binding-pipeline | `python3 corpus/instruments/capture-binding-check.py --root . \| grep -c records=84` | admitted / 1 | admitted / 1 |
| C0 | `python3 corpus/instruments/ok.py` | admitted / 1 | admitted / 1 |
| C1 | `python3 corpus/instruments/ok.py -- --root` | admitted / 1 | admitted / 1 |
| receipt-frontier | `python3 corpus/instruments/frontier-recheck-count.py \| head -2` | refused / 2 | refused / 2 |
| receipt-binding | `python3 corpus/instruments/capture-binding-check.py \| tail -1` | admitted / 1 | admitted / 1 |
| python-work-global-refused | `python3 corpus/instruments/capture-binding-check.py --work d` | admitted / 1 | refused / 2 |
| python-scratch-global-refused | `python3 corpus/instruments/capture-binding-check.py --scratch d` | admitted / 1 | refused / 2 |
| python-work-equals-refused | `python3 corpus/instruments/claim-package-check.py . --work=d` | admitted / 1 | refused / 2 |
| python-work-abbrev-refused | `python3 corpus/instruments/kill-rule-check.py --wo d` | admitted / 1 | refused / 2 |
| alias-zz-inside | `python3 corpus/instruments/zz-alias.py --json out.json` | refused / 2 | refused / 2 |
| alias-zz-outside | `python3 corpus/instruments/zz-alias.py --json out.json` | refused / 2 | refused / 2 |
| alias-fixture-inside | `python3 corpus/instruments/ok.py --json out.json` | admitted / 1 | refused / 2 |


## Exact retained terminal lines
Each cell below is the final stdout or stderr line from that run.
| Row | Base | Candidate |
|---|---|---|
| N1-python-root-space | `FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=N1-python-root-space` | `FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=N1-python-root-space` |
| N2-python-root-equals | `FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=N2-python-root-equals` | `FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=N2-python-root-equals` |
| N3-python-root-abbrev | `FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=N3-python-root-abbrev` | `FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=N3-python-root-abbrev` |
| N4-python-out-space | `FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=N4-python-out-space` | `FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=N4-python-out-space` |
| N5-python-out-equals | `FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=N5-python-out-equals` | `FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=N5-python-out-equals` |
| N6-python-out-abbrev | `FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=N6-python-out-abbrev` | `FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=N6-python-out-abbrev` |
| N7-python-json-space | `FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=N7-python-json-space` | `FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=N7-python-json-space` |
| N8-python-no-option-head | `FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=N8-python-no-option-head` | `FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=N8-python-no-option-head` |
| N9-python-selftest | `FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=N9-python-selftest` | `FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=N9-python-selftest` |
| N10-python-short-o | `FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=N10-python-short-o` | `FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=N10-python-short-o` |
| N11-python-output-long | `FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=N11-python-output-long` | `FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=N11-python-output-long` |
| N12-python-unknown-head | `FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=N12-python-unknown-head` | `FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=N12-python-unknown-head` |
| R1-capture-binding-root | `FIGURE-AUDIT figures=1 ok=0 stale=1 exit=1` | `FIGURE-AUDIT figures=1 ok=0 stale=1 exit=1` |
| R2-kill-rule-root | `FIGURE-AUDIT figures=1 ok=0 stale=1 exit=1` | `FIGURE-AUDIT figures=1 ok=0 stale=1 exit=1` |
| R3-frontier-count-root | `FIGURE-AUDIT figures=1 ok=0 stale=1 exit=1` | `FIGURE-AUDIT figures=1 ok=0 stale=1 exit=1` |
| R4-claim-package-json | `FIGURE-AUDIT figures=1 ok=0 stale=1 exit=1` | `FIGURE-AUDIT figures=1 ok=0 stale=1 exit=1` |
| R5-citation-ground-root | `FIGURE-AUDIT figures=1 ok=0 stale=1 exit=1` | `FIGURE-AUDIT figures=1 ok=0 stale=1 exit=1` |
| R6-gate-quote-audit-root | `FIGURE-AUDIT figures=1 ok=0 stale=1 exit=1` | `FIGURE-AUDIT figures=1 ok=0 stale=1 exit=1` |
| R7-routed-defects-root | `FIGURE-AUDIT figures=1 ok=0 stale=1 exit=1` | `FIGURE-AUDIT figures=1 ok=0 stale=1 exit=1` |
| R8-capture-binding-pipeline | `FIGURE-AUDIT figures=1 ok=0 stale=1 exit=1` | `FIGURE-AUDIT figures=1 ok=0 stale=1 exit=1` |
| C0 | `FIGURE-AUDIT figures=1 ok=0 stale=1 exit=1` | `FIGURE-AUDIT figures=1 ok=0 stale=1 exit=1` |
| C1 | `FIGURE-AUDIT figures=1 ok=0 stale=1 exit=1` | `FIGURE-AUDIT figures=1 ok=0 stale=1 exit=1` |
| receipt-frontier | `FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=receipt-frontier` | `FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=receipt-frontier` |
| receipt-binding | `FIGURE-AUDIT figures=1 ok=0 stale=1 exit=1` | `FIGURE-AUDIT figures=1 ok=0 stale=1 exit=1` |
| python-work-global-refused | `FIGURE-AUDIT figures=1 ok=0 stale=1 exit=1` | `FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=python-work-global-refused` |
| python-scratch-global-refused | `FIGURE-AUDIT figures=1 ok=0 stale=1 exit=1` | `FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=python-scratch-global-refused` |
| python-work-equals-refused | `FIGURE-AUDIT figures=1 ok=0 stale=1 exit=1` | `FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=python-work-equals-refused` |
| python-work-abbrev-refused | `FIGURE-AUDIT figures=1 ok=0 stale=1 exit=1` | `FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=python-work-abbrev-refused` |
| alias-zz-inside | `FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=alias-zz-inside` | `FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=alias-zz-inside` |
| alias-zz-outside | `FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=alias-zz-outside` | `FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=alias-zz-outside` |
| alias-fixture-inside | `FIGURE-AUDIT figures=1 ok=0 stale=1 exit=1` | `FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=alias-fixture-inside` |

## Directional deltas
Base admitted → candidate refused: python-work-global-refused, python-scratch-global-refused, python-work-equals-refused, python-work-abbrev-refused, alias-fixture-inside.
Base refused → candidate admitted: none across 31 measured rows.
All R1–R8 stayed admitted; all N1–N12 stayed refused. Four work/scratch controls changed only toward refusal.

## Realpath adversarial checks
Inside: created corpus/instruments/zz-alias.py → gate-quote-audit.py in the clone; removed after the row.
Outside: created corpus/instruments/zz-alias.py → /fast/scratch/hyaku/kasegi-r72/K72ExecSweep/outside.py (outside.py contained print('outside')); removed after the row.
Both candidate cases returned rc=2, with exact refusal lines in the evidence table.
The arbitrary zz-alias basename was already refused by base. To isolate changed realpath policy from unknown-name rejection, also replaced scratch-only ok.py with an in-directory symlink to gate-quote-audit.py: base admitted rc=1, candidate refused rc=2. That symlink was removed.
No output JSON was produced by the refused candidate alias derives.

## Scope and limitations
Only the assigned report is retained; all clone, fixture and transient output bytes are scratch-only and deleted before yield.
No tool installations, no network fetches, no commits, no build/lint/formatter/selftest runs.
No implementation/refactor performed; LSP was not used for this command-only investigation.
The table establishes admission parity, not correctness of the counters’ derived values. Historical symlink artifacts were excluded from the archive; no claim is made about executing those artifacts.
