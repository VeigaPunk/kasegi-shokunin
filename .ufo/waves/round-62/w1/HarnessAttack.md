# HarnessAttack — round 62 predata runner review

Axes: depth:verifiability directly; coverage not exercised. No canonical judgment, admission, integration, score change or sandbox claim.

## Reproduced counterexamples

Base `f7dcab84b104ccc03083fa1ad8c38e12830d25c9` contains the unchanged r61 runner and figure-audit instrument. Read-only `git show` extraction measured:

- `.ufo/waves/round-61/controls/c1-probe-run-r61.sh`: sha256 `bd5ac6054479aba578db855122afd2f9627a464bbc8b56d6d50f1ae9e71932f4`.
- `corpus/instruments/figure-audit.py`: sha256 `051083a2dd3b76f96568dd2a18866975b71dd1578992546c671faf21e99418a9`.

Exact argv, complete stdout/stderr, exit statuses, fixture data, environment and post-state are persisted in `.ufo/waves/round-62/w1/HarnessAttack/repro-r61-runner-defects.json`. Commands below abbreviate only the common prefixes: `R=/fast/scratch/hyaku/kasegi-r62/HarnessAttack/runner-r61.sh`, `I=/fast/scratch/hyaku/kasegi-r62/HarnessAttack/figure-audit.py`, `S=/fast/scratch/hyaku/kasegi-r61/HarnessAttack-r62`. Every subprocess used cwd and TMPDIR `/fast/scratch/hyaku/kasegi-r62/HarnessAttack`.

| Counterexample / command | Observed output and status | Smallest safe correction |
|---|---|---|
| `bash "$R" "$S/self-delete/instrument.py" "$S/self-delete"` | Runner exit **0**; empty `sha256=`; eight Python ENOENT records with `exit=2 markers=0`; stderr `sha256sum: .../self-delete/instrument.py: No such file or directory`. Instrument and scratch directory both absent afterward. | Reject resolved instrument equal to or below resolved scratch before deletion; compute/check digest without a masking pipeline. |
| `bash "$R" /fast/scratch/hyaku/kasegi-r62/HarnessAttack/broken.py "$S/broken-run"` where instrument is `raise SystemExit(99)` | Runner exit **0**; all eight records `exit=99 markers=0`, no output/reason. | Compare every named case against expected exit, marker count and semantic result/reason; any mismatch must make final status nonzero. |
| `bash -c 'find() { return 71; }; export -f find; exec bash "$@"' dependency-probe "$R" "$I" "$S/missing-find"` | Runner exit **0**; eight normal-looking records, all `markers=0`, despite failed marker collection. | Propagate collection exceptions/status; remove unchecked pipelines or enable and handle pipefail. |

These are fixable detector defects under the intended C1, not evidence against C2 or proof of unrestricted execution safety. Their impact is false evidence/provenance: empty digest, failed collection and broken instrument must not be represented as a successful predicate verdict.

Static mechanisms in identical runner bytes: instrument existence checked at lines14–17 before scratch deletion at18, without containment rejection; digest pipeline at21; probe status captured at34–36; `find | wc -l` at37 under `set -eu` without pipefail (12); successful record echo at38 supplies each function's final status. Probe calls43–54 do not assert tuples.

## Controls and boundary limits

- Normal runner: exit0; P1–P4 refuse (`exit=2 markers=0 reason=derive-not-read-only`), P5/P6/quoted-semicolon/plain-count controls pass (derived35/35/35/1). Eight records, no claim beyond named cases.
- Missing args: exit2, `HARNESS-USAGE want-instrument-and-scratch`.
- Missing instrument: exit2, `HARNESS-USAGE not-a-file .../not-found.py`; existing `keep/sentinel` retains `retain` afterward.
- Exported `python3() { return 127; }`: runner exits127 before probe records. This fixture-setup failure is correctly nonzero, contrasting the failed-find collector.
- Symlink instrument located inside scratch but resolving to a real instrument outside: exit0 and correct records; resolved real instrument survives, scratch symlink disappears. Thus containment checks should reason about resolved file identity, not merely an alias's lexical location.
- An optional readonly-scratch exploration was aborted by `FileNotFoundError` in my driver after the runner's cleanup removed the chmod target. It supplies no readonly-path verdict; no such result is claimed.

## Scope / process limits

The pinned runner accepts only `/fast/scratch/hyaku/kasegi-r61/*/*`, so exact-byte reproduction could not use the assigned r62 scratch root for its own scratch argument. I recreated the absent r61 root and used only fresh seat-unique `HarnessAttack-r62` children there. **This is a literal scratch-path contract deviation**, not an authorized exception: the assignment specified r62-only scratch. All runner deletions stayed inside that fresh subtree; no sibling, production or source-repository deletion was attempted. Commands/outputs were preserved rather than modifying the historical runner's guard. Main should not characterize this seat as fully path-conformant.

Production instrument, runner, history and indexes intentionally unchanged. Read round61 lesson, verifier spotcheck, QUALITY (including R72/R77/R79/R82), and SCORECARD planned62. No installs/updates or service restarts; no commits/pushes; no subagents. Only assigned focused harness checks exercised; no unrelated suites.

## Proposed r62 runner — independent focused review

Reviewed `w1/ExecHarness/c1-probe-run-r62.py`, sha256 `dc6303bde13abb1ffc424a8f0a3ef5f80f0f88bc4c66a4408ed8857d6d7644aa`; copied those bytes into my scratch for execution. Full exact argv/output in `.ufo/waves/round-62/w1/HarnessAttack/r62-draft-review.json`.

| Focused check | Observed |
|---|---|
| Base instrument, baseline mode | exit0, `HARNESS probes=10 failures=0 mode=baseline` |
| Base instrument, candidate mode | exit1, `HARNESS probes=10 failures=1 mode=candidate` |
| Broken instrument (`SystemExit(99)`), candidate mode | exit1, 10 failures |
| Instrument below scratch | exit2, `HARNESS-ERROR ValueError: instrument-under-scratch`; original instrument remains present |
| `collect_markers` with missing root | `FileNotFoundError` propagates; outer main catches OSError and returns2 (latter static reading) |
| Wrong-identity/recorded-output instrument | **exit0, 10 failures=0**, despite every emitted figure/refusal naming `WRONG-ID` and admitted results claiming `recorded=999` |

The draft repairs the assigned three mechanisms: resolved containment before deletion (77–84), digest from bytes read before deletion (85,100), no shell/find pipeline (63–67), explicit return/count/diagnostic comparisons and nonzero mismatch status (125–135). Its named baseline is correctly r62 base, not r61's earlier vulnerable base. No exported-find dependency remains, so invoking the old find-function injection against this Python collector would not test a dependency it uses.

**Remaining counterexample: semantic diagnostic binding is weaker than the case identity.** Line126 requires only `diagnostic in output`. The wrong-identity fixture reads each ledger and emits:

```python
if f['id'] in ('inside','inside-normalized','quoted-separator','plain-count'):
    print('FIG WRONG-ID recorded=999 derived='+f['want']+' ok')
    raise SystemExit(0)
print('FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=WRONG-ID')
raise SystemExit(2)
```

All marker counts are0, satisfying candidate tuples. Thus a result that does not attest the requested figure or recorded value can receive10/10. This does **not** defeat a predicate explicitly limited to the published `(exit, regular-marker count, diagnostic substring)` tuple; it defeats describing that tuple as full semantic per-figure verification. Smallest safe correction before freeze: bind an exact FIG/refusal record to the expected id, recorded value and derived value (and reject contradictory duplicate result records), or explicitly retain substring-only discrimination as a residual. Merely checking the instrument digest does not make a weak semantic matcher stronger. No expectation that an arbitrary malicious instrument can be made trustworthy or sandboxed is asserted.

All candidate findings were sent directly to ExecHarness for prefreeze disposition; this report reviews only the digest above, not future edited bytes. No production changes or canonical verdict issued.

## Cleanup and limits of delivery

Persisted the exact wrong-identity fixture as `.ufo/waves/round-62/w1/HarnessAttack/wrong-id.py`. Cleanup command `rm -rf -- /fast/scratch/hyaku/kasegi-r62/HarnessAttack /fast/scratch/hyaku/kasegi-r61/HarnessAttack-r62 && rmdir -- /fast/scratch/hyaku/kasegi-r61` exited0 with no output; the recreated empty r61 root was removed too. The path deviation above remains disclosed, not erased by cleanup.

Self-evaluation of this report (not canonical judgment): accuracy4 (full receipts distinguish observed from static); completeness4 (all assigned repros and available draft reviewed; no review of future bytes); clarity4 (counterexamples and corrections explicit, raw logs separate); actionability4 (exact fixtures/argv persisted; integrator must choose semantic binding before freeze); conciseness4 (detailed receipts intentionally external). Mean4.0. Main should pin any subsequently corrected draft and independently exercise its final named predicate; no such future run is claimed here.
