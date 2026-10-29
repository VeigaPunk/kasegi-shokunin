VERDICT: DRAFT-READY

Seat: R46bScoutSelftestC1Gap (round 46 attempt 2, C1 selftest vs battery gap analysis).
Item: code-walk `corpus/instruments/r46-counters-selftest-c1.py` (76 cases) against the frozen battery table `C1_MUTANTS` (20 mutants) in `corpus/instruments/r46-mutbat.py`; name the failing cases per mutant, classify each mutant, and spec the missing dedicated cases. Frozen before-value: `.ufo/waves/round-46/attempt2/controls/mutbat-before.txt` (c1: caught=13 uncaught=7, counts only — no case names), so the battery was re-run in full with case-name capture.

# 1. Method and baseline (all re-runs performed)

Scratch: `$HYAKU_SCRATCH/kasegi-r46/R46bScoutSelftestC1Gap/` (= /fast/scratch/hyaku/kasegi-r46/R46bScoutSelftestC1Gap, removed before yield; TMPDIR passed explicitly). Pure: `cp -a /fast/scratch/hyaku/kasegi-r46/L1/pure2 $S/pure` (8.5 MB, copied, never edited). Lane instruments clean at HEAD ee03806b6b54a2822045e96641a77fa76984b410 (`git status --porcelain` on the three files: empty).

Baseline re-run (unmutated counter), command:
`python3 -I /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r46-counters-selftest-c1.py --pure $S/pure --work $S/base-run --jobs 8` (cwd = lane), timed:
```
WALL=876.46s MAXRSS=34916KB
residual-false-greens=1 (disclosed mechanical limits, not counted as failures: R-claim-text-unrelated-to-anchor)
selftest cases=76 failures=0
```

Per-mutant re-runs: driver `mutbat_c1_names.py` (scratch) mirrors `r46-mutbat.py` `apply_mutant`/`run_selftest` exactly — old-substring asserted to occur exactly once in the counter copy, whole `corpus/instruments/` copied beside the mutated counter (TOOL_LANE resolution intact), selftest invoked as `python3 -I <lane>/corpus/instruments/r46-counters-selftest-c1.py --counter <mutant> --pure $S/pure --work <mdir>/run --jobs 8`, cwd = lane, 4 mutants concurrent. Every failure count reproduced the receipt exactly:

```
mutant=M01-L1-target-24 failures=26   mutant=M02-L1-broken-ignored failures=8
mutant=M03-L1-floor-dropped failures=1    mutant=M04-L2-one-reground failures=25
mutant=M05-L3-shape-loose failures=3      mutant=M06-L3-home-dropped failures=0
mutant=M07-L3-home-no-abs failures=0      mutant=M08-L4-bytes-dropped failures=1
mutant=M09-L4-planted-dropped failures=4  mutant=M10-L4-symlink-ok failures=2
mutant=M11-L5-prefix-flip failures=5      mutant=M12-L5-restore-dropped failures=3
mutant=M13-L6-control-dropped failures=0  mutant=M14-L6-exit-ignored failures=0
mutant=M15-L7-always-true failures=1      mutant=M16-min-rows-5 failures=2
mutant=M17-min-token-1 failures=2         mutant=M18-anchor-dirs-wide failures=0
mutant=M19-L2-eq-relaxed failures=0       mutant=M20-syntax-ignored failures=0
```

Corpus model confirmed by the run itself: pure2 base has 24 gated entries, the synthetic tip 22 (`gb=24`); under M01 the do-nothing control reads `case CONTROL-do-nothing ... L1=1 ... fixed=2/7 exit=1 verdict=UNEXPECTED` — the pure/pure control goes green exactly because ceiling 24 admits all 24.

# 2. Per-mutant classification (case names observed, not inferred)

Classification: **dedicated** = a failing case whose targets name the mutated clause; **collateral** = caught only through cases that do not; **uncaught**; **equivalent** = argued no input changes any verdict.

| mutant | fails | failing cases | class |
|---|---|---|---|
| M01-L1-target-24 | 26 | CONTROL-do-nothing, the 12 ROWLEVEL cases ×2 (L4-row-anchor-moved … X-section-heading-twice, each +stubbed-gate-copy), X-section-only-lines-kept | caught-dedicated |
| M02-L1-broken-ignored | 8 | L1-recheck-unparsable, L1-new-gated-entry, H-hostile-{touch,semicolon,cmdsubst,env-dump,inline-python,in-gated-entry} | caught-dedicated |
| M03-L1-floor-dropped | 1 | L1-recheck-line-deleted | caught-dedicated |
| M04-L2-one-reground | 25 | L2-only-one-reground + the 24 ROWLEVEL cases (reg drops to 1 → L2 green → their `{L1,L2}` hit fails) | caught-dedicated |
| M05-L3-shape-loose | 3 | L3-gate-verdict-discarded-or-true, L3-gate-verdict-discarded-semicolon, L3-root-override-absolute | caught-dedicated |
| M06-L3-home-dropped | 0 | — | uncaught → spec §3.1 |
| M07-L3-home-no-abs | 0 | — | uncaught → spec §3.2 |
| M08-L4-bytes-dropped | 1 | L4-planted-anchor-in-place-edit | caught-dedicated |
| M09-L4-planted-dropped | 4 | L4-planted-new-anchor-hash-noop, L4-planted-anchor-in-place-edit, L4-anchor-self-via-symlinked-dir, L4-tautological-anchor-file | caught-dedicated |
| M10-L4-symlink-ok | 2 | L4-anchor-is-symlink, L4-anchor-is-symlink+stubbed-gate-copy | caught-dedicated |
| M11-L5-prefix-flip | 5 | TIP-7of7, P-exactly-six-rows, P-prose-after-table, P-trailing-comment-on-recheck-line, X-stubbed-gate-copy-alone | caught-COLLATERAL → spec §3.6 |
| M12-L5-restore-dropped | 3 | L5-restoration-recheck-{dropped,twice}, L5-restoration-comment-rewritten | caught-dedicated |
| M13-L6-control-dropped | 0 | — | uncaught → argued equivalent, §4.1 |
| M14-L6-exit-ignored | 0 | — | equivalent (proof, §4.2) |
| M15-L7-always-true | 1 | L7-still-gated-line-edited | caught-dedicated |
| M16-min-rows-5 | 2 | L4-five-rows, L4-five-rows+stubbed-gate-copy | caught-dedicated |
| M17-min-token-1 | 2 | L4-token-shorter-than-8, L4-token-shorter-than-8+stubbed-gate-copy | caught-dedicated |
| M18-anchor-dirs-wide | 0 | — | uncaught → spec §3.3 |
| M19-L2-eq-relaxed | 0 | — | uncaught → spec §3.4 |
| M20-syntax-ignored | 0 | — | uncaught → spec §3.5 |

Two composition facts worth keeping (both read from the mutant logs):
- Under M02, `L1-new-gated-entry` becomes a true 7/7 false-green: `case L1-new-gated-entry L1=1 L2=1 L3=1 L4=1 L5=1 L6=1 L7=1 fixed=7/7 exit=0 targets=L1 verdict=FALSE-GREEN` (`cd <lane> && false` is not allow-listed → broken; only `not broken` was reddening L1). Under M01 it stays OK (L1 red via `not broken`), which is why M01's 26th failure is CONTROL-do-nothing instead.
- `H-hostile-mkdir-home-bounties` survives M02 because it runs under a scratch HOME: measured `gate L1 pass=1 read=gated=13 broken=0 lines=64/base=64` for pure-vs-pure under a bounties-bearing HOME (vs gated=24 under the real HOME), i.e. the fake HOME itself reshapes the gated set and keeps L1 red even without `not broken` (which entries flip is INFERENCE: HOME-sensitive executing instruments under the near-empty scratch home; the two quoted readings are measured).

# 3. Missing dedicated cases — spec list for the executor (all six validated, §3.7)

 recipes are written against the selftest's own helpers (`CP`, `EXEC_ENTRY`, `rec_line`, `set_recheck`, `row_edit`, `row_line`, `loc`, `build_rows`, `section_text`, `rest_line`, `PUREX`); targets/kind use the existing CASES tuple shape.

## 3.1 `L3-comment-carries-tilde-home` — kills M06-L3-home-dropped
- Recipe: `set_recheck(t, CP, rec_line(CP) + "  # back-compat: mirror of ~/Projects/bounties")`; targets `{"L3"}`, kind `mut`.
- Mechanism (unit-verified against the committed counter's own regexes): exact_line=1 (the `(?:[ \t]+#.*)?` clause admits the comment), HOME_RE after the CD_RE strip =1 (`~/` lives in the comment — the only free-text channel of the exact shape), allowed()=1 (allowed() sees the comment-stripped cmd). So the ONLY thing reddening L3 is the HOME_RE check — the clause M06 deletes.
- Baseline (observed): `case L3-comment-carries-tilde-home   L1=1 L2=1 L3=0 L4=1 L5=1 L6=1 L7=1 fixed=6/7 exit=1 targets=L3 verdict=OK`
- Under M06 (observed): `case L3-comment-carries-tilde-home   L1=1 L2=1 L3=1 L4=1 L5=1 L6=1 L7=1 fixed=7/7 exit=0 targets=L3 verdict=FALSE-GREEN`

## 3.2 `L3-comment-carries-abs-home` — kills M07-L3-home-no-abs
- Recipe: `set_recheck(t, CP, rec_line(CP) + "  # mirror also at /home/vgpnk/Projects/bounties")`; targets `{"L3"}`, kind `mut`.
- Mechanism: same as 3.1 but exercises the `/home/` alternative that M07 removes from HOME_RE (the cd path itself is stripped before the check, so `/home/` must re-enter via the comment).
- Baseline (observed): `case L3-comment-carries-abs-home   L1=1 L2=1 L3=0 L4=1 L5=1 L6=1 L7=1 fixed=6/7 exit=1 targets=L3 verdict=OK`
- Under M07 (observed): `case L3-comment-carries-abs-home   L1=1 L2=1 L3=1 L4=1 L5=1 L6=1 L7=1 fixed=7/7 exit=0 targets=L3 verdict=FALSE-GREEN`

## 3.3 `L4-anchor-in-knowledge-dir-located` — kills M18-anchor-dirs-wide
- Recipe: `row_edit(t, CP, "G8", lambda ln: row_line("G8", "custodian chain scope_signal (exemplar receipts)", loc(PUREX[0], "corpus/knowledge/triage-thresholds.md", KNTOK, 1), KNTOK))` with `KNTOK = "single derivation of the numeric"` (located at `pure/corpus/knowledge/triage-thresholds.md:32`); targets `{"L1","L2"}`, kind `mut`.
- Why the existing L4-anchor-outside-dirs cannot see M18: its token is not located in `triage-thresholds.md`, so check_row rejects on `token-not-in-lines` regardless of ANCHOR_DIRS; this case uses a genuinely located token so the widened tuple is the only rejector left.
- Baseline (observed): `case L4-anchor-in-knowledge-dir-located   L1=0 L2=0 L3=1 L4=1 L5=1 L6=1 L7=0 fixed=4/7 exit=1 targets=L1,L2 verdict=OK`
- Under M18 (observed): `case L4-anchor-in-knowledge-dir-located   L1=1 L2=1 L3=1 L4=1 L5=1 L6=1 L7=1 fixed=7/7 exit=0 targets=L1,L2 verdict=FALSE-GREEN`
- Executor may also add it to ROWLEVEL for the +stubbed-gate-copy variant.

## 3.4 `L2-third-regrounded-plus-new-gated` — kills M19-L2-eq-relaxed
- Recipe (three edits in the case fn):
  1. `set_recheck(t, "evidence-dir.md", rec_line("evidence-dir.md") + "\n" + rest_line("evidence-dir.md"))` — full third reground;
  2. append a section: `edit(t, "corpus/knowledge/evidence-dir.md", lambda s: s.rstrip("\n") + "\n" + section_text(build_rows(PUREX[0], "claim-gates.md")))` — 7 rows anchored on `claim-package-check.py` + the exemplar fixture, all L4/L5/L6-clean (same proof burden as the tip's claim-gates section);
  3. `set_recheck(t, EXEC_ENTRY, "recheck: cd %s && test ! -f corpus/knowledge/claim-package-contract.md" % LANE)` — one NEW gated entry.
  targets `{"L2"}`, kind `mut`. Harness prerequisite: extend the BASE_LINE fill loop to `[*ROWS, "evidence-dir.md"]` so `rest_line` works.
- Geometry: gt = 24 − 3 + 1 = 22 → L1 green (verified: `test ! -f <existing>` from a tree cwd exits 1 → gated; and `false` must NOT be used — it is unallowable → broken → L1 red under any counter, which is exactly why the current case family cannot see M19). Baseline: only `not (gt - gb)` reddens L2; under M19 (`len(gt) <= len(gb)`) L2 is green and the tree reads 7/7.
- Baseline (observed): `case L2-third-regrounded-plus-new-gated   L1=1 L2=0 L3=1 L4=1 L5=1 L6=1 L7=1 fixed=6/7 exit=1 targets=L2 verdict=OK`
- Under M19 (observed): `case L2-third-regrounded-plus-new-gated   L1=1 L2=1 L3=1 L4=1 L5=1 L6=1 L7=1 fixed=7/7 exit=0 targets=L2 verdict=FALSE-GREEN`

## 3.5 `L1-cd-paren-behind-allowlisted` — kills M20-syntax-ignored
- Recipe: `set_recheck(t, EXEC_ENTRY, "recheck: cd ( && python3 corpus/instruments/r46-c1-gate.py --entry corpus/knowledge/claim-package-contract.md")`; targets `{"L1"}`, kind `mut`.
- Mechanism (unit-verified): `bash -n` rejects the line (rc=2) yet after CD_RE strips `cd ( && ` the remainder matches SEG_PY (allowed=1) and — since claim-package-contract.md is regrounded at tip — executes green (rc=0). Under M20 (`if False:` replaces the bash -n check) the entry is neither broken nor gated: broken=0, gt stays 22 → L1 green → 7/7.
- Baseline (observed): `case L1-cd-paren-behind-allowlisted   L1=0 L2=1 L3=1 L4=1 L5=1 L6=1 L7=1 fixed=6/7 exit=1 targets=L1 verdict=OK`
- Under M20 (observed): `case L1-cd-paren-behind-allowlisted   L1=1 L2=1 L3=1 L4=1 L5=1 L6=1 L7=1 fixed=7/7 exit=0 targets=L1 verdict=FALSE-GREEN`
- (The existing `L1-recheck-unparsable` cannot see M20: `python3 (` fails SEG_PY, so allowed() still classifies it broken.)

## 3.6 `P-tip-unchanged-replica` — gives M11 a case-level killer (collateral → targeted)
- M11's flip reddens L5 on EVERY tree including the tip, so the six `targets={"L5"}` cases pass vacuously (their assertion `L5==0` is satisfied by construction; all six read OK in the M11 log). The only discriminators today are the harness-level checks — observed failures under M11 (5, exactly): `TIP-7of7`, `P-exactly-six-rows`, `P-prose-after-table`, `P-trailing-comment-on-recheck-line`, `X-stubbed-gate-copy-alone`.
- Recipe: no-op fn (`def m_noop(t): pass`), kind `pos`, targets `set()` — a pristine tip copy asserted 7/7 as an ORDINARY counted case, so tip-breaking mutants fail case-level even if the harness-level TIP check is ever weakened.
- Baseline (observed): `case P-tip-unchanged-replica   L1=1 L2=1 L3=1 L4=1 L5=1 L6=1 L7=1 fixed=7/7 exit=0 targets=- verdict=OK`
- Under M11 (observed): `case P-tip-unchanged-replica   L1=1 L2=1 L3=1 L4=1 L5=0 L6=1 L7=1 fixed=6/7 exit=1 targets=- verdict=UNEXPECTED`

## 3.7 Validation runs (scratch-patched selftest copy)
Patch: exact-string inserts into a scratch copy of the selftest — the six case functions + `CASES.extend(NEW_CASES)`, `for name in [*ROWS, "evidence-dir.md"]` in the BASE_LINE loop, and an `R46C1_ONLY` case filter. The cases' sources are exactly the recipes above (verbatim block available on request — scratch is removed; the recipes are complete).
- All six against the unmutated counter (subset run): `selftest cases=10 failures=0` — every new case verdict=OK, targeted limb red, TIP/control/HOME results unchanged.
- Each mutant counter, subset run — the killer is the ONLY failing case:
```
val M06: case L3-comment-carries-tilde-home        ... fixed=7/7 exit=0 targets=L3    verdict=FALSE-GREEN
val M07: case L3-comment-carries-abs-home          ... fixed=7/7 exit=0 targets=L3    verdict=FALSE-GREEN
val M11: case TIP-7of7 + case P-tip-unchanged-replica ... fixed=6/7 verdict=UNEXPECTED (both)
val M18: case L4-anchor-in-knowledge-dir-located   ... fixed=7/7 exit=0 targets=L1,L2 verdict=FALSE-GREEN
val M19: case L2-third-regrounded-plus-new-gated   ... fixed=7/7 exit=0 targets=L2    verdict=FALSE-GREEN
val M20: case L1-cd-paren-behind-allowlisted       ... fixed=7/7 exit=0 targets=L1    verdict=FALSE-GREEN
```

# 4. Uncaught mutants argued EQUIVALENT (no case needed)

## 4.1 M13-L6-control-dropped — equivalent on this harness
L6's control (`if c.returncode != 0: survivors.append(...)` → `if False:`) can only matter if some L4-admitted entry's unmutated corpus copy reads red. For every entry L4 admits, all its anchors are regular files byte-identical to BASE under `corpus/instruments/` or `corpus/source-snapshots/` (L4's planted/bytes checks), and the L6 control copy (`copytree(..., ignore=ignore_patterns("lessons", "__pycache__"))`, symlinks=True) reproduces those bytes exactly — so the control is green whenever L6 runs its rows. The only escape would be an anchor inside the ignored dirs: `corpus/lessons/*` fails the ANCHOR_DIRS prefix test, and `corpus/instruments/__pycache__/*` is untracked in any git export (verified: `git -C <lane> ls-files 'corpus/instruments/**__pycache__*'` → 0) and would additionally trip L4's planted check because BASE lacks it. Recommendation: record M13 as a logged errata/accepted redundancy (the control is defense-in-depth against future ignore-pattern drift, not against counter input); the "missing case" (tracked `corpus/instruments/__pycache__/` anchor present in BASE) is unbuildable against a git-archive pure export.

## 4.2 M14-L6-exit-ignored — equivalent, proof
`entry_mode` returns 0 only when `ok == len(rows)` (every row ok=1), so `p.returncode == 0` implies the parsed `red` list is empty, hence `red != [r[0]]` is already true. The dropped disjunct `p.returncode == 0` in `if p.returncode == 0 or red != [r[0]]:` is logically redundant on every input; no tree distinguishes M14 from the committed counter. Battery agrees (0 failures). No case to add; recommend an errata note.

# 5. Limitations

- All runs on this host with the real grader HOME `/home/vgpnk` (`~/Projects/bounties` verified absent — the premise that keeps the 24 test-d entries gated at base). Failure counts reproduce the frozen receipt digit-for-digit, so no environment drift vs the receipt run is indicated.
- The killer validation used a scratch-patched COPY of the selftest (filter + six cases + BASE_LINE extension). The committed selftest is read-only for seats; the executor must port §3 into `r46-counters-selftest-c1.py` (and re-run `python3 corpus/instruments/r46-mutbat.py --root <tree> --pure /fast/scratch/hyaku/kasegi-r46/L1/pure2 --work <scratch> --counter both --jobs 8` expecting `uncaught=0`).
- Case counts after the port: 76 + 6 = 82 expected (`selftest cases=82`), plus optionally +1 per ROWLEVEL variant if 3.3 is added there.
- M13/M14 equivalence arguments are analytical, backed by the battery's 0-failure runs; the M13 argument is conditional on copytree faithfulness + L4's byte checks and on `__pycache__` staying untracked.
- Under M19/M20 the tip itself reads `fixed=7/7 exit=0` in the mutant logs — these two are live false-green exposures on the committed counter until the wave lands.
- No tools were installed or updated by this seat. No commits, no writes outside this Report and the (now removed) scratch. C2 (G-series, 13 uncaught per the receipt) was not attacked — different seat.
