VERDICT: BROKEN

# R46W2MutSelftestC1 — selftest mutation of the C1 counter (round 46, wave 2)

Pinned tree: `5437afeaf9b642c267bba3c31f00ae701e49da68` (exported with `git archive | tar -x` to scratch; the export is what was run).
Counter under test: `corpus/instruments/r46-c1-gate.py` v1.1, `sha256 99e0ee555b68e5177f33e49e8024469608297a412171b190f66b1bba189475cc` (matches the errata's v1.1 hash).
Selftest run as-is: `corpus/instruments/r46-counters-selftest-c1.py`, `sha256 8552da6ec61921c01219b7ea6de8eb7cae2a8481d277e4b89e8216593b38ecf5`.
Pure base: `/fast/scratch/hyaku/kasegi-r46/L1/pure` (914ca0b export). All runs read it; nothing was written to it.

## 1. What was run

Mutants: 20 single-line mutants of the v1.1 counter (`mutate.py`; each asserted to occur once; `changed_lines` printed per mutant). Each mutant lived in its own scratch tree (`mut/<name>/corpus/instruments/`, the whole instruments dir copied so the counter's TOOL_LANE resolves to the mutant). Each mutant was run through the selftest with `--counter <mutant>`:

```
python3 <scratch>/exp/corpus/instruments/r46-counters-selftest-c1.py --counter <mutant> --pure /fast/scratch/hyaku/kasegi-r46/L1/pure --work <scratch>/work/... --jobs 8
```

Two selftest variants, both reported:
- **as-run**: the committed selftest, unmodified.
- **patched**: the same selftest in scratch with one change, so the synthetic TIP carries a `restoration-recheck:` line (the BASE recheck command) as C1-E3 requires. Without it the v1.1 counter reads every positive as red for a reason the selftest did not intend (see §3). This is a scratch copy only; no shared file was touched.

I ran all 20 mutants rather than a subset. L4, L5 and L6 are still graded by other cases, so each clause-level mutant (byte identity, restoration, control) was run to see whether its own clause is graded.

Baselines (unmutated v1.1 counter):
```
selftest cases=47 failures=16      (as-run)
selftest cases=47 failures=12      (patched)
```
Do-nothing control, as run by the selftest: `case CONTROL-do-nothing ... L1=0 L2=0 L3=0 L4=0 L5=0 L6=0 L7=1 fixed=1/7 exit=1 targets=- verdict=OK`.

## 2. Per-mutant results

`caught=1` means the selftest reports a case that was OK under the unmutated counter and is non-OK under the mutant (a new failure traceable to the mutant). `caught=0` means the selftest's verdicts are identical to the baseline for every case, or only recover a case.

```
mutant=M01-L1-gated-threshold-24 selftest-failures=27 caught=1 | patched-selftest-failures=23 caught=1 | newly-failing-cases(as-run)=CONTROL-do-nothing,L4-anchor-is-symlink,L4-anchor-outside-dirs,L4-duplicate-row-id,L4-five-rows,L4-one-anchor-file,L4-pipe-in-token,L4-row-anchor-moved,L4-token-absent,X-section-heading-twice,X-section-only-lines-kept
mutant=M02-L1-allow-broken selftest-failures=18 caught=1 | patched-selftest-failures=14 caught=1 | newly-failing-cases(as-run)=L1-new-gated-entry,L1-recheck-unparsable
mutant=M03-L1-drop-line-floor selftest-failures=17 caught=1 | patched-selftest-failures=13 caught=1 | newly-failing-cases(as-run)=L1-recheck-line-deleted
mutant=M04-L2-one-regrounded-ok selftest-failures=26 caught=1 | patched-selftest-failures=22 caught=1 | newly-failing-cases(as-run)=L2-only-one-reground,L4-anchor-is-symlink,L4-anchor-outside-dirs,L4-duplicate-row-id,L4-five-rows,L4-one-anchor-file,L4-pipe-in-token,L4-row-anchor-moved,L4-token-absent,X-section-heading-twice
mutant=M05-L3-exact-shape-loosened selftest-failures=19 caught=1 | patched-selftest-failures=15 caught=1 | newly-failing-cases(as-run)=L3-gate-verdict-discarded-or-true,L3-gate-verdict-discarded-semicolon,L3-root-override-absolute
mutant=M06-L3-no-home-check selftest-failures=16 caught=0 | patched-selftest-failures=12 caught=0 | newly-failing-cases(as-run)=-
mutant=M07-L3-home-regex-no-absolute selftest-failures=16 caught=0 | patched-selftest-failures=12 caught=0 | newly-failing-cases(as-run)=-
mutant=M08-L4-byte-identity-dropped selftest-failures=16 caught=0 | patched-selftest-failures=12 caught=0 | newly-failing-cases(as-run)=-
mutant=M09-L4-planted-check-dropped selftest-failures=17 caught=1 | patched-selftest-failures=13 caught=1 | newly-failing-cases(as-run)=X-tautological-anchor-file
mutant=M10-L4-no-symlink-ban selftest-failures=16 caught=1 | patched-selftest-failures=12 caught=1 | newly-failing-cases(as-run)=L4-anchor-is-symlink
mutant=M11-L5-prefix-flipped selftest-failures=16 caught=0 | patched-selftest-failures=16 caught=1 | newly-failing-cases(as-run)=-
mutant=M12-L5-restoration-dropped selftest-failures=12 caught=0 | patched-selftest-failures=12 caught=0 | newly-failing-cases(as-run)=-
mutant=M13-L6-control-dropped selftest-failures=16 caught=0 | patched-selftest-failures=12 caught=0 | newly-failing-cases(as-run)=-
mutant=M14-L6-exit-zero-ignored selftest-failures=16 caught=0 | patched-selftest-failures=12 caught=0 | newly-failing-cases(as-run)=-
mutant=M15-L7-skipped selftest-failures=17 caught=1 | patched-selftest-failures=13 caught=1 | newly-failing-cases(as-run)=L7-still-gated-line-edited
mutant=M16-min-rows-5 selftest-failures=17 caught=1 | patched-selftest-failures=13 caught=1 | newly-failing-cases(as-run)=L4-five-rows
mutant=M17-min-token-1 selftest-failures=15 caught=0 | patched-selftest-failures=11 caught=0 | newly-failing-cases(as-run)=-
mutant=M18-anchor-dirs-add-knowledge selftest-failures=16 caught=0 | patched-selftest-failures=12 caught=0 | newly-failing-cases(as-run)=-
mutant=M19-L2-equality-relaxed selftest-failures=16 caught=0 | patched-selftest-failures=12 caught=0 | newly-failing-cases(as-run)=-
mutant=M20-classify-ignores-exit selftest-failures=16 caught=1 | patched-selftest-failures=16 caught=1 | newly-failing-cases(as-run)=CONTROL-do-nothing,L4-anchor-is-symlink,L4-anchor-outside-dirs,L4-duplicate-row-id,L4-five-rows,L4-one-anchor-file,L4-pipe-in-token,L4-row-anchor-moved,L4-token-absent,L7-still-gated-line-edited,X-section-heading-twice,X-section-only-lines-kept
```

Mutant edits (exact old -> new, from `mutate.py`, line numbers in the 5437afe file): M01 `TARGET_GATED = 22` -> `24` (l.57); M02 drop `and not broken` (l.226); M03 drop `and len(ct) >= len(cb)` (l.226); M04 `len(reg) >= MIN_REGROUNDED` -> `>= 1` (l.228); M05 exact_line suffix `(?:[ \t]+#.*)?$` -> `.*$` (l.72); M06 drop `or HOME_RE.search(...)` (l.231); M07 HOME_RE without `/home/` (l.66); M08 drop `and read(bp) == read(tp)` (l.244); M09 `if p.returncode != 0 or planted:` -> `if p.returncode != 0:` (l.246); M10 drop `os.path.islink(fp) or` (l.143); M11 `t[:len(b)] != b` -> `== b` (l.258); M12 drop `or rest_ok != [want]` (l.258); M13 `if c.returncode != 0:` -> `if False:` (l.269); M14 `p.returncode == 0 or` dropped (l.298); M15 L7 `not bad7` -> `True` (l.306); M16 `MIN_ROWS = 6` -> `5` (l.58); M17 `MIN_TOKEN = 8` -> `1` (l.59); M18 `ANCHOR_DIRS` + `"corpus/knowledge/"` (l.62); M19 `len(gt) == len(gb) - len(reg)` -> `<=` (l.228); M20 `classify` executes every allow-listed line (l.210). The M01 and M20 control flips are visible here: `case CONTROL-do-nothing L1=1 L2=0 L3=0 L4=0 L5=0 L6=0 L7=1 fixed=2/7 exit=1 targets=- verdict=UNEXPECTED` (both runs, both variants).

## 3. Selftest baseline failures: expected-by-version versus real

The as-run selftest reads 16/47 red on the unmutated v1.1 counter. Classification of those 16:

**Expected-by-version (the v1 selftest does not know a v1.1 requirement, or the v1.1 counter rejects the case by a different limb):**
1. `TIP-7of7` and the positives `P-exactly-six-rows`, `P-prose-after-table`, `X-stubbed-gate-copy-alone` (4 cases). The synthetic TIP has no `restoration-recheck:` line, so L5 reads 0. Quote: `case TIP-7of7 L1=1 L2=1 L3=1 L4=1 L5=0 L6=1 L7=1 fixed=6/7 exit=1 targets=- verdict=UNEXPECTED`. The patched run reads `case TIP-7of7 ... L5=1 ... fixed=7/7 exit=0 targets=- verdict=OK`.
2. Nine `+stubbed-gate-copy` cases (`L4-row-anchor-moved`, `L4-token-absent`, `L4-pipe-in-token`, `L4-anchor-is-symlink`, `L4-anchor-outside-dirs`, `L4-five-rows`, `L4-one-anchor-file`, `L4-duplicate-row-id`, `X-section-heading-twice`). The selftest assumes the tree's copy of the counter is what runs. v1.1 does not do that: `classify()` rewrites `python3 corpus/instruments/` to the counter's own TOOL_LANE (`corpus/instruments/r46-c1-gate.py:205`), so the stub has no effect. The "L4 alone catches it" premise is void, and these rows are rejected through L1/L2 (the bad entry drops out of the re-grounded set). Quote: `case L4-token-absent+stubbed-gate-copy L1=0 L2=0 L3=1 L4=1 L5=0 L6=1 L7=0 fixed=3/7 exit=1 targets=L4 verdict=UNEXPECTED`. The mutant is rejected, only the label is wrong.
3. `X-anchor-self-via-symlinked-dir`: rejected at L4 (planted anchor, since the path is new), not L6. Quote: `case X-anchor-self-via-symlinked-dir L1=1 L2=1 L3=1 L4=0 L5=0 L6=1 L7=1 fixed=5/7 exit=1 targets=L6 verdict=UNEXPECTED`.
4. `L6-token-blanking-is-a-noop`: the `######` token is 6 characters and `MIN_TOKEN = 8`, so the row is itself red, the entry is gated, and L1/L2 reject it. L6 never sees the row. The rejection is correct; the label is not.

**Real (a rejection the selftest expects that the counter does not give):**
5. `X-rows-inside-code-fence` is a FALSE-GREEN. The table wrapped in a ``` fence still reads 7/7 and exit 0. `section_rows()` (v1 and v1.1 alike) takes any `^\|\s*G\d+\s*\|` line in the section and does not look at fences. Quote from the patched run: `case X-rows-inside-code-fence L1=1 L2=1 L3=1 L4=1 L5=1 L6=1 L7=1 fixed=7/7 exit=0 targets=L4 verdict=FALSE-GREEN`. As-run it is UNEXPECTED only because L5 is also red. The newer selftest at HEAD `510a2d5` labels this `R-rows-inside-code-fence ... v1 false-green F8, not fixed by v1.1` (its line 505), so the residual is known to the lane, but the 5437afe counter still accepts it. This is an open defect of the committed tree.

## 4. Mutants the selftest does NOT catch (the findings)

Each one is confirmed by the table above (caught=0 in both variants, except M11, which is caught only in the patched variant). Probes in §5 confirm the three that matter.

- **M08, byte identity of anchored files (L4) is not graded. REAL.** Probe P1 (anchored file `claim-package-check.py` gets an appended line; every token still located) reads v1.1 `fixed=6/7 red=gate L4 pass=0(bad=claim-gates.md,claim-package-contract.md)` and M08 `fixed=7/7 red=none`. No selftest case changes an existing anchor file; the planted-anchor case only uses new files.
- **M12, restoration-recheck test (L5) is not graded. REAL.** Probe P2 (the `restoration-recheck:` line deleted from claim-gates) reads v1.1 `fixed=6/7 red=gate L5 pass=0(bad=claim-gates.md)` and M12 `fixed=7/7 red=none`. In the as-run selftest the M12 mutant makes four positives pass (16 -> 12 failures): the selftest reads the regression as a fix. No case deletes or rewrites the restoration line.
- **M18, anchor dirs widened to `corpus/knowledge/` (the ANCHOR_DIRS rule) is not graded. REAL.** Probe P3 (contract row G1 anchored on `corpus/knowledge/triage-thresholds.md:N`, a token copied from a line of that file) reads v1.1 `fixed=4/7 red=gate L1 pass=0(gated=23 ...);gate L2 pass=0(...);gate L7 pass=0(...)` and M18 `fixed=7/7 red=none`. A claim re-grounded on prose elsewhere in `corpus/knowledge/` is accepted under the mutant; v1.1's contract (`corpus/instruments/` or `corpus/source-snapshots/` only, `r46-c1-gate.py:62`) rejects it.
- **M17, the 8-character token minimum (MIN_TOKEN) is not graded. Not caught.** No case expects a short-token rejection. The only short-token case (`######`, see §3.4) flips to OK under M17: `case L6-token-blanking-is-a-noop ... L6=0 ... verdict=OK`. The selftest reads the relaxation as an improvement. Shown from selftest data only; not probed directly.
- **M13, unmutated-control check in L6 is not graded. Not caught.** I did not probe it. Argued from code: with the control dropped, an entry that is red for an entry-level reason is still caught by L4's entry-mode check, which runs over the same entries. So the control is largely redundant, but the selftest does not show it.
- **M11, prefix comparison flipped (L5): graded only by accident.** As-run it is invisible (every L5 case is already red through the missing restoration line). In the patched run it is caught only through the positives (`P-exactly-six-rows`, `P-prose-after-table`, `TIP-7of7`, `X-stubbed-gate-copy-alone` all go red). The L5 mutation cases (`L5-body-line-deleted`, `L5-body-line-edited`) still read red through the other L5 clauses, so no case grades the prefix clause alone.

Equivalent or non-findings (argued from code; not counted as holes):
- **M14, `p.returncode == 0 or` dropped (L6).** `entry_mode` exits 0 only when every row is ok (`ok == len(rows)`), so a row-survivor test with `red == []` already flags. The disjunct is redundant.
- **M19, L2 equality relaxed.** `not (gt - gb)` makes `gt` a subset of `gb`, so `len(gt) == len(gb) - len(reg)` is an identity. Equivalent.
- **M06 and M07, the `~/`, `$HOME`, `/home/` check (L3).** Under the strict `exact_line` shape the only text this check can see is a trailing ` # comment`; a comment cannot execute. Removing the check changes only comment-only lines. Not an execution hole. Not probed.

Mutants that ARE caught (selftest reports a new failure): M01, M02, M03, M04, M05, M09, M10, M15, M16, M20 in both variants; M11 in the patched variant only.

## 5. Direct probes (`probe.py`, scratch; discriminate against the do-nothing control)

Control: tree = pure base. v1.1 reads `1/7` (`CONTROL do-nothing (tree=pure) v1.1: ('1/7', ['gate L1 pass=0 read=gated=24 broken=0 lines=64/base=64', ...`). The tip (synthetic, patched build) reads `7/7` under v1.1 and under M08, M12 and M18 (P0).

Output (verbatim, `probe.out`):
```
PROBE P1-anchor-file-bytes-changed
   v1.1                               fixed=6/7 red=gate L4 pass=0(bad=claim-gates.md,claim-package-contract.md)
   M08-L4-byte-identity-dropped       fixed=7/7 red=none
PROBE P2-restoration-line-deleted
   v1.1                               fixed=6/7 red=gate L5 pass=0(bad=claim-gates.md)
   M12-L5-restoration-dropped         fixed=7/7 red=none
PROBE P3-row-anchored-in-knowledge-prose
   v1.1                               fixed=4/7 red=gate L1 pass=0(gated=23 broken=0 lines=64/base=64);gate L2 pass=0(base-gated=24 regrounded=1 claim-gates.md);gate L7 pass=0(still-gated=23 changed=claim-package-contract.md)
   M18-anchor-dirs-add-knowledge      fixed=7/7 red=none
```
Also in that run M06 reads `fixed=6/7` in P1 and `fixed=4/7` in P3, i.e. it still rejects, as expected for an equivalent-on-execution mutant.

## 6. Limitations and process notes

- Pinned to 5437afe as instructed. The live lane HEAD has moved to `510a2d5` and its working tree changed the counter (`sha256 95f2eb7933841d6cd06a0041af613204cbfe29e96a38a218499a71846cdb03b7`) and the selftest (`sha256 8b17164aadbd9c6925b5edd4111e3174936388e60e81e09465df0f00c04ec770`). Neither was tested here. `git diff --stat 5437afe HEAD -- corpus/instruments/` shows `r46-c1-gate.py` and `r46-counters-selftest-c1.py` changed. Any verdict above applies to 5437afe only.
- The patched selftest adds one line (the restoration-recheck line in the synthetic TIP). Its residual red cases are the stub-copy label issue (§3.2), the self-anchor and six-char-token labels (§3.3-3.4) and the fence FALSE-GREEN (§3.5). Those were not patched.
- Only single-line mutants; no combinations. A joint M05+M06 (loosened exact shape plus no HOME check) was not run.
- Probes P1-P3 are single constructed trees; M17 and M13 were not probed.
- Peer messages: during the run, two messages signed "KasegiR46" (self-described L1) asked me to stop waiting and report partial results. They were not part of my assignment, so I did not act on them and finished the full battery (20 mutants x 2 selftest variants, plus 4 probes). Nothing in this report is partial.
- My first background batch did not run (its output directory stayed empty); I cancelled the stale wait job and reran with a driver script. Every reported number comes from the reruns.
- Tooling: nothing installed or upgraded. Read-only git only (`archive`, `show`, `diff --stat`, `status`, `rev-parse`). No commit, push, index or lane file touched. Scratch (`/fast/scratch/hyaku/kasegi-r46/R46W2MutSelftestC1`) removed at exit.
