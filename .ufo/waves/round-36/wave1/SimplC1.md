# SimplC1 — r36-closure.sh dead-surface review (round 36, depth:verifiability)

Seat: SimplC1 (simplifier). Item: review the drafted `corpus/instruments/r36-closure.sh`
for YAGNI/dead surface and propose a minimal deletion diff that keeps E1-E9 + `--selftest`
intact. Review target (read-only, not in the lane):

- path: `/fast/scratch/hyaku/kasegi-r36/ExecC1SuiteBuild/r36-closure.sh` (author: ExecC1SuiteBuild)
- sha256: `ff616adc045a8938c7ca69b3693565ef0f676a0d1d67df293b1b6c4a82da4720`
- size: 737 lines; `bash -n` clean (author's claim re-verified here: rc=0)

Verdict: 5 deletion sites, net −19 lines (737 -> 718), plus 2 documentation-truth fixes.
Measured behavior identical on every tree available this round; `--selftest` on a synthetic
green head gives `cases=9 failures=0` exit 0 with the same 9 case lines and the same mutant
counts (3/3, 2/2, 3/3, 1/1, 1/1, 1/1, 1/1, 2/2, 3/3).

The author refroze three times while this review ran; the **final** bytes are
`4db1ae70c76afd28b29e9ec24c2e44835322c61fa33e30c966f75ce0dfadb7c4` (894 lines). See "Third pass"
for the review of those bytes: no dead function/local remains, cuts 1/5/6 from this list are in,
the survivors the critics found are closed, and the suite measures `closed=9/9 exit=0` +
`cases=9 failures=0` on a synthetic final head. The only residual duplication is a 3-line banner
written in two places (~3 lines); not worth another freeze.

Minimal copy I actually ran: scratch `r36-min.sh`, sha256
`fc3287635908afacc58ad9dddf830a0977c5ab6bb12f4e0d60c31296a55c92b6`, 718 lines, `bash -n` rc=0.
The lane file was never edited; the author (ExecC1SuiteBuild) was sent the cut list and owns
the edit.

## Method and tool availability

- `bash -n` on the frozen draft and on the minimal copy: rc=0 both.
- Reference/caller proof: no LSP server speaks shell here — the `lsp` device is not mounted
  (`read xd://lsp` -> "No such tool"; the mounted-device list has no language server), so no
  semantic `references` answer exists for these shell functions. Caller analysis is therefore
  definition/use counting over the file plus execution: every proposed deletion was applied to
  a scratch copy and the nine checks + selftest were re-run, which is the only reference proof a
  bash script admits. Recorded as a limitation, not presented as semantic proof.
- Symbol scan: each `^name()` definition counted against `\bname\b` uses; `local` declarations
  scanned for zero `$var`/`${var}` uses. Result: zero unused functions and zero unused locals
  (the two scanner hits `commit`/`fixture` in `selftest_case_E9` are text inside the
  `git ... commit -m fixture` fixture command, not declarations).
- Trees measured (each a `git -C <lane> archive <ref> | tar -x` export in scratch, or a scratch
  clone-of-`.git` fixture):
  - `3266c9937b03062d9bbc2f436e20820115ed179c` (r35 base)
  - `0aee0ef105395a2f1d6ace7eaeef13871bb26988` (r35 judged head)
  - `b47f2cdf17d9f6021cbdb4db1add09a9dbf4f1d6` (round-36 claims-freeze head = lane HEAD today)
  - synthetic green head: scratch repo built by copying the lane's `.git` (read-only copy) and
    committing two fixture commits on top of `b47f2cdf` that add the still-missing closing bits
    (E3 registry rows, E4 provenance note, E8 round-36 lesson with `M36`, and a `Final lane
    commit:` line naming the fixture's own parent). Toplevel of that repo was verified equal to
    the scratch dir before any `git add`/`commit`; the lane repo was never touched. This is the
    only way to exercise the green path before the round closes.

## Proposed deletions (line anchors = frozen 737-line draft)

1. `run_check`, lines 396-407 — the `case $id in ... esac` dispatch is a second registry of
   E1-E9 living beside `CHECK_IDS=(E1..E9)`, so adding/renaming a check needs two edits and the
   two can disagree (unknown id silently becomes `unknown-check` payload, which the summary
   then reads as `closed=0`). Replace the body with `"check_${id,,}" "$@"`.
   Net −11 lines. Verified: all nine checks still run and report (dispatch exercised by every
   run below) — bash 5 `${id,,}` maps `E1` -> `check_e1`.
2. Lines 680-686 — the `forge-caselines` block is a third forgery artefact that trips the *same*
   first condition in `judge_selftest_report` as `forge-summary`: both files have zero
   `^selftest case=` lines, so both are rejected for missing case lines, not for their summary
   text. Keep the two distinct limbs (`forge-summary` = the summary-only spelling the kill rule
   names; `forge-failed-cases` = 9 case lines with `verdict=fail`); drop this duplicate spelling.
   −7 lines; selftest loses exactly one `selftest judge=forged-caselines rejected=1` line and
   still reports `cases=9 failures=0` exit 0.
3. `check_e4`, lines 298/300/301/303/304 — drop the `tracked-index` limb (`git -C "$LANE"
   ls-files`). It is the only live-index read left in E1-E8 (the header's "never reads the live
   worktree" cannot cover it), and it is redundant with the export-scoped proof the claim asks
   for: `ls-tree -r --name-only <ref> -- <path>` = 1. It can only add false negatives (a dirty
   index beside a clean exported ref at filing). Also delete the two doc clauses that describe
   it (line 18 `ls-files,`; lines 67-69). −4 code lines, −2 doc lines.
4. Lines 735-737 — `if [ "${BASH_SOURCE[0]}" = "$0" ]; then main "$@"; fi`. Nothing sources the
   file and no selftest stub uses it (the selftest drives check functions, never the entry
   guard). Call `main "$@"` directly. −2 lines. (Kept the flag, not the dead mode: there is no
   `--root`, no live-run, no JSON mode to remove.)
5. Documentation truth (delete a false sentence, add the true one; no code change):
   - line 9 "The suite never reads the live worktree" is false — E9 limb (a) is
     `git status --porcelain` on the lane and limb (c) is `rev-parse HEAD`. Replaced with
     "every check reads only under the export root; the sole live reads are E9's quiescence
     limbs, which are live by definition".
   - lines 87-88 "it is what makes the r35 base export read 0/9 rather than 8/9" — measured
     counterfactual below; the number is 1/9, not 8/9. Limb (c) stays (it is load-bearing), the
     justification is corrected: without (c), limbs (a)+(b) read E9 closed for *any* export on a
     quiescent machine, so the r35 base export would print `closed=1/9` instead of the frozen
     `closed=0/9`.
   - line 276 `grep -cE '201\.2'` -> `grep -cF '201.2'` (no metacharacter intended; fixed-string
     is the honest form). Cosmetic, included because the neighboring E2 limb already uses `-cF`.

Net: 737 -> 718 lines (34 content lines deleted, 16 added, the rest of the diff is the doc
rewrites above).

## Evidence — parity of the minimal copy against the frozen draft

Same flags/tree, frozen vs minimal, per-check `closed=` flags identical (the only payload key
removed is the deleted `tracked-index`):

| tree | frozen | minimal | flag parity |
|---|---|---|---|
| `3266c993` (r35 base) | `closed=0/9 exit=1` | `closed=0/9 exit=1` | E1-E9 identical |
| `0aee0ef1` (r35 judged head) | `closed=4/9 exit=1` | `closed=4/9 exit=1` | E1-E9 identical |
| `b47f2cdf` (lane HEAD) | `closed=5/9 exit=1` | `closed=5/9 exit=1` | E1-E9 identical |
| synthetic green head | `closed=9/9 exit=0` | `closed=9/9 exit=0` | E1-E9 identical |
| green head `--selftest` | `cases=9 failures=0` exit 0 | `cases=9 failures=0` exit 0 | 9 case lines identical |
| lane HEAD `--selftest` (pre-closure) | n/a | `cases=9 failures=4` exit 1 | honest: E3/E4/E8/E9 positives still open |

Exact commands (scratch paths; lane read-only):

```
bash r36-frozen.sh --export-ref <hash> --work <scratch>/w1
bash r36-min.sh    --export-ref <hash> --work <scratch>/w2
bash r36-min.sh    --export-ref HEAD --lane <scratch>/green --scratch-root <scratch>/greenscratch --work <scratch>/w3
bash r36-min.sh    --selftest --export-ref HEAD --lane <scratch>/green --scratch-root <scratch>/greenscratch --work <scratch>/w4
```

Per-check parity diff used `grep -oE '^E[1-9] payload=.* closed=[01]$|^closed=.*'` and stripped
`,tracked-index=[0-9]+` from the frozen payloads; all four trees matched line for line.

`--help` diff between frozen and minimal contains only the three intended doc rewrites (E4 limb,
E9 rationale, export-mode sentence). Measured help size: frozen 104 lines / sha256 `e0f0fb2bd99d0b61ed634b30a699d17e8ba2a5e952d0e7502434a87925e1507e`;
minimal 106 lines / sha256 `dd05a3d0ed0e810b111e2892830f7a4751a113eeb689ca59f80fb8efed235485`.
The whole help block is generated from the header comment, so the two doc-line deletions and the
two doc-line additions are the entire delta; no help text is dropped.

## Head-match counterfactual (measured, corrects the draft's note)

Scratch variant of the frozen draft with limb (c) neutralised (`head_ok` dropped from the pass
condition), run against a quiescent repo (clean worktree) and an empty scratch root:

- `--export-ref 3266c993…` -> `E9 payload=status-dirty=0,scratch-seat-dirs=0,head-match=0
  closed=1`, `closed=1/9 exit=1`
- `--export-ref 0aee0ef1…` -> E9 same, `closed=5/9 exit=1`

So (c) is required for the frozen base expectation `closed=0/9` (otherwise 1/9), and the draft's
"rather than 8/9" is arithmetically impossible: without (c) the maximum on any historical export
is E9 alone (+ the historical E2/E5/E6/E7 at the judged head) = 1/9 and 5/9. Keep the limb, fix
the sentence.

## Considered and deliberately retained

- `count_lines` — not dead: `grep -c .` reads empty input as 0, whereas `wc -l` reads
  `printf '%s\n' ""` as 1 and would make `check_e6`'s "zero candidate paths" case indistinguishable
  from one candidate. It is load-bearing on E4/E6/E9.
- `run_suite_report`'s self-agreement checks (`n -ne 9`, `counted -ne k`) — tautological today
  because every payload is one line, but they are the printed report's own honesty check on an
  axis judged by report text. Removing them buys 8 lines and risks a future multi-line payload
  printing a summary that disagrees with its lines. Not proposed.
- `--lane` / `--scratch-root` — both exercised above (green positive limb without touching the
  lane); not dead surface.
- `judge_selftest_report`'s distinct-id loop — `cases==9` + `verdicts==9` alone admit nine copies
  of one id; the loop is the only limb that pins the nine ids. Keep.
- `CHECK_IDS` itself — after cut 1 it is the single registry; keep (do not also fold it into the
  selftest function names).

## Residual risk I could not close without the closing bytes

E1 binds *every* 40-hex value on a `Final lane commit:` line or the four lines after it, and
requires all of them to resolve and be ancestors (`bound -eq total`, `total -ge 1`). At
`b47f2cdf` this is 4/4 bound (the r33 hash, the wave-1 integration hash, the r34 closing hash,
and the r35 closing hash), so the limb is green today. If the L1's round-36 closing sentence puts
another commit's 40-hex within four lines of the marker (e.g. "wave-1 integration commit `…`.
**Final lane commit: `…`**"), E1 will require that commit to be an ancestor too and can go red on
otherwise-good bytes. The frozen claim says "the Final lane commit line's hash" (singular); the
implementation is stricter than the claim. Not a deletion (it fails closed and currently passes),
flagged so the L1 can decide whether to scope it to the last marker.

## Second pass — the refrozen draft (817 lines)

After the first pass the author refroze the instrument:

- sha256 `76273416f7a6668a702eadf5a6c03b80ae87ad4793f652880303fcb7f8230323`, 817 lines, 34631 bytes,
  `bash -n` rc=0 (re-verified here).
- Disposition of my cuts: **1 adopted** (`run_check` is now `"check_${id,,}" "$@"` with a one-line
  comment), **5 adopted** (the header no longer claims the suite never reads the live worktree and
  names the sole live reads), **6 adopted** (the staleness-limb counterfactual is now the measured
  1/9 base / 5/9 judged head). **2, 3, 4 kept with author reasons** I can verify but not overrule:
  `forge-caselines` is the literal claim-shaped summary-only forgery (`cases=9 failures=0` with no
  case lines), so its rejection is evidence for the frozen wording; `tracked-index` is mandated
  verbatim by the seat's own spec (`git ls-files .ufo/waves/round-35/wave1-results.json` = 1) and
  ANDed with the ref-scoped `ls-tree` limb (stricter, never looser); the `BASH_SOURCE` guard is
  how the author's harness and the sibling seats source the file for per-check probes — it has
  callers outside my view, so it is not dead in practice.
- New surface reviewed for dead weight, none found: `e3_registry_rows` (one awk, used twice;
  section-scoped, and its mention/outside-registry mutants are proved), the E7 row-shaped regex
  (both limbs green on the real `QUALITY.md` rows at `0aee0ef1` and `b47f2cdf`), E8's
  `names-corrected-line` and `round35-lesson` limbs (both meaningful: a lesson that records a
  correction without naming the corrected instrument, and a missing round-35 lesson reading as
  "stale line absent"), E9's `lane-root` limb (rejects a status repo that is a subdirectory of an
  enclosing repository) and `--no-optional-locks` (keeps the status read from writing
  `.git/index.lock` under the lane). `sroot_state` is payload evidence, not a gate — legitimate.
  Re-scanned for unused functions/locals: none (the only text hits are `shift` builtins and the
  dynamically dispatched `check_e*`/`main`, which are reached by name derivation and file scope).
- Re-measured with this frozen draft (fresh scratch, same tree set): `3266c993` -> `closed=0/9
  exit=1`; `0aee0ef1` -> `closed=4/9 exit=1`; `b47f2cdf` -> `closed=5/9 exit=1`; synthetic final
  head (real lane `.git` copied to scratch, closing bits committed: E3 registry rows, E4
  provenance note, round-36 lesson with `M36` and the `source-recheck` correction) ->
  `closed=9/9 exit=0` and `--selftest` exit 0, `cases=9 failures=0`, mutant counts
  `3/3, 2/2, 5/5, 1/1, 1/1, 1/1, 2/2, 4/4, 4/4`.
- Tradeoff accepted with cut 1: the `case` dispatch was the statically greppable call-site list;
  after the cut, `grep check_e3` finds only the definition. The compensation is that `CHECK_IDS`
  is the single registry and the nine selftest cases exercise every check by name each run, which
  the green selftest above demonstrates. Nothing else in the file changed by the cut.
- Two closing-seat dependencies the author's new limbs make explicit (not defects, but the L1 and
  the scribes must know them or the final 9/9 cannot happen): E3 needs table ROWS whose first cell
  is exactly `r35-defect-closure.sh` / `r36-closure.sh` inside a `## …Gates & probes registry…`
  section (a prose mention or a row under another heading is correctly rejected), and E8 needs
  the round-36 lesson to contain the literal token `source-recheck` as well as `M36`.
  ScribeMistakes's planned M36-2 row quotes the `source-recheck exit 0 on committed bytes` line,
  so that token is on the planned path; the E3 rows were still absent from `SKILL.md` at
  `b47f2cdf` (row counts 0/0), which is the known closing-seat obligation.

## Third pass — the final refreeze (894 lines)

The author froze again after CritC1Kill/MutC1Fixtures survivors:

- sha256 `4db1ae70c76afd28b29e9ec24c2e44835322c61fa33e30c966f75ce0dfadb7c4`, 894 lines, `bash -n` rc=0
  (re-verified here). Changes: E1 is scoped to the round-36 SCORECARD block (`e1_has_round36` +
  `e1_final_hashes` from the last `Round[- ]36` heading to EOF), E2 requires the erratum marker
  and the corrected row (`| depth:density | 9 | mean **201.2**`), E4/E5 require non-empty files
  (`-s`), and the judge cross-checks detail lines (`det == n`, `rej == ok`, `ok == n`, n >= 1).
- Re-measured (fresh scratch): `3266c993` -> `closed=0/9 exit=1`; `0aee0ef1` -> `closed=3/9
  exit=1`; `b47f2cdf` -> `closed=4/9 exit=1`; synthetic final head (real lane `.git` copied
  read-only, closing bits plus a `## Round 36` SCORECARD block whose `Final lane commit:` line
  names the fixture's parent) -> `closed=9/9 exit=0`; `--selftest` exit 0,
  `cases=9 failures=0`, mutant counts `4/4, 3/3, 5/5, 1/1, 1/1, 1/1, 2/2, 4/4, 4/4`, and four
  forged reports rejected (`forged-summary`, `forged-caselines`, `forged-failed-cases`,
  `forged-detail-free`) plus the own report accepted.
- Dead-surface scan of the 894-line bytes: no unreferenced function, no unused local (the
  `check_e*` names are reached by `"check_${id,,}"`, the selftest cases by
  `"selftest_case_${id}"`, `main` at file scope; the remaining text hit is the `shift` builtin).
  `suite_digest` is called twice and printed in both banners — evidence, not dead code.
- Remaining duplication, reported but not pressed: the 3-line banner
  (`export-ref=… lane=… suite-sha256=…` plus the two `deviation=` lines) is written twice — in
  `run_suite_report` and in `main`'s selftest branch. Factoring it into one helper saves ~3 lines
  with no behavior change; I do not propose another freeze cycle for that, since each refreeze
  costs the reviewers a re-measure and the duplication cannot disagree (same three variables,
  same order).
- E1's earlier residual (all 40-hex within four lines of a marker must bind) is now scoped: only
  the round-36 block's `Final lane commit` lines bind, so a history-only closure is correctly
  red. It is still "all such lines in the block", which is the intended fail-closed reading and
  is green on the fixture; the only new landing obligation is that the round-36 SCORECARD block
  must contain a resolvable, ancestor `Final lane commit:` line.
- Closing-seat dependencies now explicit in this version: E3 registry rows (0/0 at `b47f2cdf`),
  E4 provenance note must exist and be non-empty, E8 needs `M36` + literal `source-recheck` in
  the round-36 lesson, E2 needs the round-35 erratum marker (present, `marker=1`) and the
  corrected row (present, `row=1`), E1 needs the round-36 block with a bound hash.
- Export-tree constraint behind the explicit-path design (ExecC1ExportMode, same digest): the
  export carries 58 committed symlinks with absolute live-lane targets, so any recursive or
  glob-driven check would follow them into the lane. Every check in these bytes names its files
  explicitly (E3's awk and E7's row greps included); that is a correctness constraint, not
  missing generality, and no proposed cut touches it.

## Scope / hygiene

- Lane writes: this receipt only. Every experiment ran on scratch copies of the lane export; the
  lane repo itself was read with `git archive|rev-parse|ls-tree|ls-files|status` only.
- Scratch root `/fast/scratch/hyaku/kasegi-r36/SimplC1/` removed after this receipt was written.
- Tooling: nothing installed, nothing upgraded (no need; bash/coreutils/git sufficed).
- Route chain at spawn kept; no swarm, no `agent://all`.

## Appendix — unified diff of the first-pass minimal version (a = the superseded 737-line draft, b = minimal)

The author froze a new draft afterwards (`76273416…`, 817 lines) and adopted cuts 1, 5 and 6
from this list; see "Second pass" above. This appendix documents the first-pass diff exactly as
measured, so the rejected cuts keep their evidence.

```diff
--- a/corpus/instruments/r36-closure.sh
+++ b/corpus/instruments/r36-closure.sh
@@ -6,7 +6,9 @@
 # is CLOSED and non-zero while it is still OPEN, so the suite is a fail-closed
 # gate over the bytes of a named lane head.
 #
-# EXPORT MODE IS THE ONLY RUN MODE. The suite never reads the live worktree:
+# EXPORT MODE IS THE ONLY RUN MODE. Every check reads only under the export
+# root; the sole live reads are E9's quiescence limbs, which are live by
+# definition (worktree status, scratch leftovers, standing HEAD).
 # `--export-ref <hash>` extracts the lane tree with
 #   git -C <lane> archive <hash> | tar -x -C <scratch>/export
 # and every check reads only under that export root. A plain run (no
@@ -15,7 +17,7 @@
 # The only ref-scoped git reads that cannot be answered from the export bytes —
 # E1's commit existence/ancestry, E4's tracking lints, E9's quiescence — are
 # read-only git subcommands against the lane repo (archive, rev-parse, cat-file
-# -e, merge-base --is-ancestor, ls-tree, ls-files, status). Nothing is written
+# -e, merge-base --is-ancestor, ls-tree, status). Nothing is written
 # under the lane; the only writes are the extraction and the selftest fixtures
 # under --work (or a mktemp dir honouring TMPDIR), both removed on exit.
 # --work must lie outside the lane; its `export/` and `mut/` subdirectories are
@@ -63,9 +65,8 @@
 #       `r-defect-closure.sh`, the round-33/34 instrument, which is why the
 #       exact-basename row is a separate check.
 #   E4  `.ufo/waves/round-35/wave1-results.json` is tracked at the exported ref
-#       (`ls-tree -r --name-only <ref> -- <path>` = 1 line) AND in the lane index
-#       (the frozen `git ls-files` limb = 1 line) AND the provenance note
-#       `<path>.provenance.md` exists in the export beside it.
+#       (`ls-tree -r --name-only <ref> -- <path>` = 1 line) AND the provenance
+#       note `<path>.provenance.md` exists in the export beside it.
 #   E5  `.ufo/waves/round-35/claims-erratum-d5.md` exists in the export.
 #   E6  The round-34 wave-1 integration receipt carries the appended
 #       `Correction (round 35)` note. The receipt path is derived from the
@@ -84,8 +85,9 @@
 #       -maxdepth 1 -type d` empty, the suite's own --work dir excluded by
 #       absolute path); (c) the exported ref IS the lane's standing HEAD
 #       (`rev-parse HEAD`), so an export of a stale commit cannot read quiescent.
-#       Limb (c) is the staleness guard: it is what makes the r35 base export
-#       read 0/9 rather than 8/9 on a machine with no scratch leftovers.
+#       Limb (c) is the staleness guard: on a quiescent machine limbs (a)+(b)
+#       alone read E9 closed for any export, so without (c) the r35 base export
+#       would print closed=1/9 (E1-E8 are all zero there), not the frozen 0/9.
 #
 # Documented limits (measured, not hidden):
 #   - E1 matches the two placeholder spellings the round-35 spot-check and this
@@ -273,7 +275,7 @@
     cd "$tree" || { printf 'tree-unreadable'; exit 2; }
     local row mean
     row=$(grep -cF -- 'round-34 depth:density row' SCORECARD.md 2>/dev/null); row=${row:-0}
-    mean=$(grep -cE -- '201\.2' SCORECARD.md 2>/dev/null); mean=${mean:-0}
+    mean=$(grep -cF -- '201.2' SCORECARD.md 2>/dev/null); mean=${mean:-0}
     printf 'erratum-row=%s,erratum-mean=%s' "$row" "$mean"
     [ "$row" -ge 1 ] && [ "$mean" -ge 1 ] && exit 0
     exit 1
@@ -295,13 +297,12 @@
 
 check_e4() { # TREE REF
   local tree=$1 ref=$2 p=.ufo/waves/round-35/wave1-results.json
-  local t_ref t_idx note=0
+  local t_ref note=0
   t_ref=$(git -C "$LANE" ls-tree -r --name-only "$ref" -- "$p" 2>/dev/null | count_lines)
-  t_idx=$(git -C "$LANE" ls-files -- "$p" 2>/dev/null | count_lines)
-  t_ref=${t_ref:-0}; t_idx=${t_idx:-0}
+  t_ref=${t_ref:-0}
   if ( cd "$tree" && [ -f "$p.provenance.md" ] ) 2>/dev/null; then note=1; fi
-  printf 'tracked-ref=%s,tracked-index=%s,provenance-note=%s' "$t_ref" "$t_idx" "$note"
-  [ "$t_ref" -eq 1 ] && [ "$t_idx" -eq 1 ] && [ "$note" -eq 1 ] && return 0
+  printf 'tracked-ref=%s,provenance-note=%s' "$t_ref" "$note"
+  [ "$t_ref" -eq 1 ] && [ "$note" -eq 1 ] && return 0
   return 1
 }
 
@@ -393,18 +394,7 @@
 
 run_check() { # ID TREE REF [EXTRA...]
   local id=$1; shift
-  case $id in
-    E1) check_e1 "$@" ;;
-    E2) check_e2 "$@" ;;
-    E3) check_e3 "$@" ;;
-    E4) check_e4 "$@" ;;
-    E5) check_e5 "$@" ;;
-    E6) check_e6 "$@" ;;
-    E7) check_e7 "$@" ;;
-    E8) check_e8 "$@" ;;
-    E9) check_e9 "$@" ;;
-    *) printf 'unknown-check:%s' "$id"; return 2 ;;
-  esac
+  "check_${id,,}" "$@"   # E1 -> check_e1: CHECK_IDS is the only registry
 }
 
 # ---------------------------------------------------------------------------
@@ -677,13 +667,6 @@
     printf 'selftest judge=forged-summary rejected=1\n'
   fi
 
-  printf 'selftest cases=9 failures=0\n' > "$WORK/forge-caselines.txt"
-  if judge_selftest_report "$WORK/forge-caselines.txt"; then
-    printf 'selftest judge=forged-caselines rejected=0\n'; rc=1
-  else
-    printf 'selftest judge=forged-caselines rejected=1\n'
-  fi
-
   {
     local i
     for i in 1 2 3 4 5 6 7 8 9; do
@@ -732,6 +715,4 @@
   esac
 }
 
-if [ "${BASH_SOURCE[0]}" = "$0" ]; then
-  main "$@"
-fi
+main "$@"
```
