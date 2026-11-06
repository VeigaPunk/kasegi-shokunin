# ReviewC1 — round-80 C1 adversarial review (recheck-cwd successor)

Seat: ReviewC1-5 (reviewer, leaf). Scope: diff vs unlanded r79 candidate; the 16 assigned rows
(N10 N11 N21 N25 N26 N27 N30 T1 T2 + K-M4 K-M5 K-W1 K-P1 K-P2 K-NP K-CL); predicates P1–P8; EXC_RE.
Frozen bytes were read only; no lane file, instrument or corpus file was written.

Frozen-hash check (all match claims.json): candidate `420151fd…5698`; mutbat `b47276d1…d450`;
table `08d7f3ce…e418`; build-table `e0a8c714…ee0ef3`; base instrument `e666ae11…ab52a21a`
(`git show 58905f2:corpus/instruments/recheck-cwd-census.py`). Lane HEAD `4ab54586`; the lane's
working-tree `corpus/instruments/recheck-cwd-census.py` also hashes `420151fd…5698`.

## Findings by severity

### Blocker
None. Every frozen row is counted killed (P3 run, below); every assigned row's failing check
matches its `expect`; P1–P8 are single commands whose output can falsify them; EXC_RE behaves as claimed.

### Major (routed to round 81; outside the frozen table, not verdict changes)
- **M1 — TMPDIR regular-file guard unexercised.** Candidate line 145
  `if tmp is not None and not os.path.isdir(tmp):`. Mutant `isdir` → `exists` **survives**
  selftest (`rc=0`; normalized output identical to the unmutated run except the scratch tag).
  Behaviour, observed on a scratch fixture lane with `TMPDIR` set to a regular file:
  candidate → `recheck-cwd: TMPDIR <file> is not a directory`, rc 2;
  mutant → `NotADirectoryError` traceback from `tempfile.mkdtemp`, rc 1. No fixture covers a
  file-valued TMPDIR, so the refusal contract (exit 2, no traceback) is not closed for that input.
- **M2 — timeout branch unexercised.** Candidate lines 94–95
  `except subprocess.TimeoutExpired: return -1`; docstring line 13 says timeouts count as `exit_other`.
  Mutant `return -1` → `return 0` **survives** selftest (`rc=0`, identical output). By code reading,
  a hanging recheck would be classed `exit0_foreign` (conformant). Not executed to the 120 s timeout
  (inference from code path plus survival). No fixture sets `TIMEOUT` low.

### Minor
- **m1 — K-CL is not the r79 transform.** Table row K-CL re-anchors `_calls` (r79: body → `return True`)
  to `_pred_call` (r80, lines 188–190: body → `return node if isinstance(node, ast.Call) else None`).
  Same class (predicate-name matcher neutered) but not "the same transform" as claims.json states for
  the seven re-anchored rows. Kill holds: `gate-predicates FAIL rows=28 expect=28 bad=[26]`.
  Correct the claims wording in round 81; bytes stay frozen.
- **m2 — N11 deletes a different row than the r79 survivor.** r79 N11 deleted the empty-rows
  polarity row; the r80 row deletes `(predicates_ok([(True, True)], 2), False)` (line 486). The kill
  comes only from the count binding (`predicates_ok` line 176, `GATE_ROWS = 28`): any single-row
  deletion gives 27 ≠ 28. Deletion together with a `GATE_ROWS` edit is a composite (routed).
- **m3 — N27 relocated.** r79 N27 dropped `and not rest7` at the case-7 call; the r80 row drops
  `and rest_ran is False` inside `both_headers_ok` (line 181). Same class; killed `bad=[21]`.
- **m4 — `expect` field is prose, unenforced.** `mutbat.py` reads only `id/anchor/replacement/class`.
  I checked all 28 failing sets by hand against `expect` (all match; see table). Verifiability gap for
  round 81: the counter should check the named check.
- **m5 — P5 not executed.** P5 runs the live-lane census (executes 93+ knowledge recheck values)
  and is meant for the landing tree. Structurally falsifiable; verification gap.
- **m6 — lane working tree is already dirty** (`git status`: SKILL.md, corpus/instruments/README.md,
  corpus/SOURCES.md, corpus/QUALITY.md, corpus/instruments/recheck-cwd-census.py, untracked
  corpus/knowledge/osv-ubuntu-binary-to-source-mapping.md). P6's `cases=15` counts (1/1) are read
  from that dirty tree. Base `cases=6` counts (1/1 pre-landing) were confirmed at `58905f2`. Informational.

## Assigned rows (mutant applied to a scratch copy; `--selftest` run with TMPDIR=scratch)
All 16 mutants: rc 1, no Traceback, normalized output differs from the unmutated run. Counter verdict
from `mutbat.py` (full run): KILLED counted=yes, except K-M3 EXCEPTION-KILL counted=yes (class `exception`).

| row | r79 source | same transform? | candidate line | failing check(s) observed | expect matches |
|---|---|---|---|---|---|
| N10 | MutC1Hunt N10-calls-recurse-true | same class (consumed() recursion accepted without name check); `return node` vs r79 `return True` | 194 | gate-predicates FAIL bad=[26] (wrong_src) | yes |
| N11 | N11-rows-drop-empty | same class (row deletion), different row (m2) | 486 | gate-predicates FAIL rows=27 expect=28 | yes |
| N21 | N21-census-exitother-to-exit1 | identical | 131 | prefix-census FAIL exit1_foreign=2 exit_other=0 | yes |
| N25 | N25-gatecheckids-firstsidelog | identical | 173 | gate-predicates FAIL bad=[11] | yes |
| N26 | N26-gatecheckids-superset | identical | 173 | gate-predicates FAIL bad=[13] | yes |
| N27 | N27-case7-drop-rest-flag | same class, relocated (m3) | 181 | gate-predicates FAIL bad=[21] | yes |
| N30 | N30-runforeign-cwd-inherit | identical | 90 | prefix-census FAIL exit0_foreign=2 exit1_foreign=2 (want 3/1) | yes |
| T1 | ReviewEquiv T1 (argument neutered) | identical | 526 | gate-wiring FAIL F4:gate-consume:526 | yes |
| T2 | ReviewEquiv T2 (RESULT ret conjunct) | identical | 393 | gate-negpolarity FAIL neg_ok=False neg_ret_ok=True | yes |
| K-M4 | K-M4 (r79 `is False`→`is True`) | identical on the 2-arg predicate | 168 | gate-predicates FAIL bad=[4,5]; gate-negpolarity FAIL | yes |
| K-M5 | K-M5 (r79 deleted case-7 check) | identical (deletes both-headers check) | 409–412 | gate-wiring FAIL F3:both-headers; gate-checkids FAIL missing=['both-headers'] | yes |
| K-W1 | K-W1 (r79 body → `return []`) | same effect; insertion before docstring | 198 | gate-predicates FAIL bad=[24,26,27] | yes |
| K-P1 | K-P1 | identical | 176 | gate-checkids FAIL side_logs=[[True],[True],[False]] | yes |
| K-P2 | K-P2 | identical | 502 | gate-wiring FAIL F1/F2/F3 (gate-predicates:502) | yes |
| K-NP | K-NP | identical | 534 | gate-wiring FAIL F1/F2/F3 (gate-negpolarity:534) | yes |
| K-CL | K-CL | **not identical** (m1) | 188–190 | gate-predicates FAIL bad=[26] | yes |

The other 12 rows (K-M1 K-M2 K-M3 K-X1 K-X2a K-X2b K-M8 K-W2 K-N1 K-G1 K-C1 K-T1) were also run; each
FAIL set matches its `expect`. K-T1's caught exception has detail `ret=-99 stdout="exception=…"`, so
it is scored KILLED (the R129 rule working as intended).

## Predicate audit (claims.json P1–P8)
| P | single command | falsifiable output | run here | result |
|---|---|---|---|---|
| P1 | yes | `selftest cases=15 failures=0` + rc | TMPDIR=`<scratch>` run: `cases=15 failures=0`, rc 0 | holds |
| P2 | yes | sha256 equality | `420151fd…5698` | holds (frozen bytes) |
| P3 | yes | `MUTBAT … killed=28 survived=0 dirty=0 notderived=0` | rc 0, `baseline=ok rows=28 killed=28` | holds |
| P4 | yes | rc 2, stderr `recheck-cwd: TMPDIR…`, no Traceback | rc 2, stderr `recheck-cwd: TMPDIR /nonexistent-kasegi-r80 is not a directory`, 0 Traceback | holds |
| P5 | yes | census line equality + five zero counters + RESULT | not run (m5) | unverified here |
| P6 | yes | grep counts (1/1 at landing; base 0/0 for cases=15, 1/1 for cases=6) | base `58905f2` confirmed cases=6 in SKILL.md and README; working tree shows cases=15 | form holds; landing count not yet observable |
| P7 | yes | `subprocess.run(` = 1, `"bash", "-c"` = 1, `"/tmp` = 0 | 1 / 1 / 0 | holds (non-tautological: 0 is a real assertion) |
| P8 | yes | `mutbat selftest ok`, rc 0 | `mutbat selftest ok … T-EXCA counted=no`, rc 0 | holds |

## EXC_RE audit
Yes, as claimed. `EXC_RE = ^selftest case=\S+ FAIL exception=` (mutbat.py line 42, re.M). A mutant
output is EXCEPTION-KILL only if some line matches it (line 64–65). It counts only for rows whose
`class` is `exception` (line 95). An assertion row whose output matches EXC_RE is therefore
EXCEPTION-KILL counted=no, and the battery marks it DIRTY, so the battery fails. The selftest
(T-EXCA) demonstrates this; T-KILL, whose detail is `note=exception-free …`, scores KILLED counted=yes,
so the free-text substring rule is gone. The only `exception=`-prefixed FAIL producers in the candidate
are lines 523 and 532 (`check(... "exception=%r" % exc)`); line 453 is a caught value whose FAIL detail
begins `ret=`. Residual leniency (negligible): `\S+` excludes case names containing whitespace; every
candidate case name is hyphenated.

## Verdict
C1-REVIEW = no-blocker
Routed to round 81: M1, M2 (survivors outside the frozen table), m1 (claims-text correction), m4
(enforce `expect`).

## Tooling and verification gaps
- No tools installed. Commands run: `diff -u`, `sha256sum`, `python3 -B mutbat.py` (full table and selftest),
  candidate `--selftest` under scratch TMPDIR, candidate `--root/--lane` with a nonexistent TMPDIR, the
  row drivers (scratch), `grep`, read-only `git -C <lane> status|show|rev-parse|log`.
- Not run: P5 (landing-tree census); the timeout path of M2 (120 s).
- The r79 survivor status (N10 … N30) is cited from round-79 MutC1Hunt.md and ReviewEquiv.md and was not
  re-run against the r79 candidate.
