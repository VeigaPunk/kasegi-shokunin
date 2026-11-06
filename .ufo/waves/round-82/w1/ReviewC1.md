# ReviewC1 — round-82 C1 review (recheck-cwd successor, r82 table, counter decoy limb)

Seat: ReviewC1 (reviewer, leaf). Read-only, except for one execution: the counter selftest (P9).
Some probes were in-process Python over strings and the counter's own
`rename_locals`. No mutant battery, forgery driver or candidate run was executed.

Frozen-byte check: sha256 candidate `81677e9d…773e050`, mutbat `a7d4db43…ac55c`, table
`045edc07…f26a`, build-table `07727196…5885`, forgery driver `52cc6be5…3908`. All five
equal claims.json:13-15. `git diff --quiet b9589300 -- .ufo/waves/round-82/{c1,controls,claims.json}`
returns clean. The worktree `corpus/instruments/recheck-cwd-census.py` already equals the
candidate (uncommitted, sha `81677e9d`). Base `1a50638e:` is `a3b58aa5`. Diff:
`ReviewC1-receipts/candidate-vs-base.diff` (+70/−11; the only code changes are `conform_ok`,
main():795, the two checks and the docstrings).

## Executed
- **P9**: `TMPDIR=$S python3 -B mutbat.py --selftest --work $S` returned rc 0 in 0.39 s with
  `mutbat selftest ok … selfdiff_forgery_exit=False`. Receipt:
  `ReviewC1-receipts/p9-mutbat-selftest.out`.
- **Table provenance**: compared `jq` row projections of the r81 table at `1a50638e` with the r82
  table. Exactly S04/S05 change anchor/replacement, and J1, S07M, B1 and B2 are appended. All
  other 57 rows are byte-identical in id, anchor, replacement, kill_cases and class.
- **J1** = r81 junk edit. `diff a5269ee:…/recheck-cwd-census.py
  round-81/w1/CriticClaims-receipts/candidate-junkedit.py` gives exactly
  `+if name.startswith("osv-"): continue` after `counts["entries"] += 1`. This matches the
  table row (build-table.py:41-43) and lesson defect 3 (round-81-verifier-spotcheck.md:104).
- **S07M** = the routed survivor. `round-80/w1/MutC1Hunt/survivors/S07.py:557` reads
  `root, lane, verbose = ".", DEFAULT_LANE, True`, and the row replaces candidate :778 with
  exactly that line. This matches r81 ReviewC1.md:43-62 Major 1 and lesson defect 5 (:106).
  Closed.
- **S04/S05**: the same conjuncts are dropped as in r81 (S04 drops `exit2_foreign == 0`, S05
  drops `norecheck == 0`), now in conform_ok :262-263. The kill case is still conform-limbs:
  case 15 isolates each limb, and neither drop affects bucket-sum (`bal`/`short` have exit2=0
  and norecheck=0).
- **B1/B2** (build-table.py:47-52): B1 drops the sum conjunct, and `conform_ok(short)` then
  returns True, which fails bucket-sum. B2 inlines the r81 four limbs in main(); the
  census-swapped main run (:643-649) then returns 0 and bucket-sum fails. Both are real kills
  of the new assertion. B1's replacement leaves `… == 0\n            )`, which is valid syntax.

## Findings

### Major
1. **The decoy limb is deterministic and unkeyed, so a byte-level forgery passes it.
   mutbat.py:38-40 "Known limit" and claims.json:16 ("rejects the enumerated byte- and
   normalized-text forgeries") understate the limit.** D1 and D2 (mutbat.py:183-184) are a pure
   function of the target bytes, with a fixed `_d` suffix (:172) and no nonce. A forger can
   precompute them. F9 is F6-selfdiff plus one constant: the sha256 of its own pre-`_FG_TABLE`
   prefix under D1 and under D2. That prefix does not depend on the constant's value, so there
   is no fixed-point problem. Simulated with the frozen counter's `rename_locals`/`ast.unparse`
   and the F6 decision logic:
   - pristine and both decoys: no FAIL;
   - all 60 non-neutral rows: case-matched hits;
   - 3 neutrals: no hits.

   Expected result: `killed=60 neutral_ok=3/3 decoy=ok` with rc 0
   (`ReviewC1-receipts/f9-hashwhitelist-sim.txt`). [INFERENCE: simulation, not run under
   mutbat; an executor run would confirm it.]

   So routed defect 2 ("a counter-owned second kill limb that rejects" forgery-selfdiff,
   spot-check :103) is met only for the unmodified F6 shape. A two-hash variant of the same
   self-diff passes. The claim's literal wording ("the enumerated …") and P4 still hold, so the
   verdict does not change. The prose and docstring should say "any detector invariant under,
   or able to precompute, the two published decoys". Route to r83:
   - Derive the decoy from a per-run secret: a random rename suffix, random local-rename
     choice, or random no-op insertion.
   - Add an F9 control.

### minor
- **m1. conform_ok's bucket-sum is tested in only one direction, so `== → >=` survives.**
  At recheck-cwd-census.py:264, the probe at :630-632 only tests `buckets < entries`
  (`short`). With `buckets >= counts["entries"]`, bal (3>=3) and short (2>=3 False) both hold,
  and every real census balances, so the selftest stays green. The docstring promise "every
  entry is accounted" holds either way. The `==` (over-count, double-bucketing) direction is
  unasserted. Census double-counting would still be caught by the exact per-bucket counts in
  prefix-census, so the gap is narrow. Fix: add a row with `buckets > entries`.
- **m2. main-default asserts only that output is silent without the flag; `--verbose` itself
  is never asserted.** No selftest run passes `--verbose` (grep shows only :787). Mutating
  :788 `verbose = True` to `False` survives. The check (:658-664) is a real assertion of the
  main()-site default it names, and it kills S07M.
- **m3. D2 does not preserve semantics in general; honest targets can wrongly show
  `decoy=broken`.** Each class below ran in-process on toy code and produced a correct original
  but a failing D2 (`ReviewC1-receipts/d2-hazard-probes.txt`).

  | class | D2 failure | cause |
  |---|---|---|
  | nested `def f` plus a local `f` elsewhere | NameError `f_d` | FunctionDef names are never renamed, but every Name load is |
  | function-local `import json` plus a local `json` elsewhere | NameError | aliases are not renamed |
  | class attribute `limit` plus a local `limit` | AttributeError | class-body stores are missed: :145-146 walks only the ClassDef node |
  | method-local class attribute | AttributeError | same cause |
  | `'%(who)s' % locals()` | KeyError | string-keyed introspection |
  | `g(**{'verbose': True})` | TypeError | :153 excludes only literal call keywords |
  | `match` capture patterns | NameError | MatchAs names are not renamed |

  More cases:
  - RecursionError on deep nesting (:185 maps it to broken).
  - D1 drops comments and normalizes quotes, so an honest selftest that greps its own source
    text (a self-lint) breaks.
  - The renaming is per identifier across the whole module, not per scope (:170-177).

  None of these affects this candidate (decoy=ok, D1 is AST-equal). The docstring's
  "semantics-preserving rewrites" (mutbat.py:22-23) is false as a general statement.
- **m4. The `h >= 1` gate is a formatting property, not an honesty property, and is weak.**
  - An honest target written in canonical `ast.unparse` style, whose anchors contain no
    renamable local, gets `decoy_hidden=0`, and the battery exits 1 (toy probe in
    d2-hazard-probes.txt).
  - Conversely, a row whose anchor survives both decoys has no decoy protection. Here that is
    1/60: M2, anchor `            return -1\n`. A text-keyed forgery can key on such rows
    freely. Only 39/60 anchors are hidden by D1 alone; D2 hides the remaining 20.

  P3 pins 59/60 exactly, so the round's verdict does not depend on the `>=1` threshold.
- **m5. The bucket-sum fixture is tailored to the known junk edit.** Its names are `osv-a.md`
  and `osv-b.md` (:634-635), matching J1's prefix.
  - The general guard is real: main()'s conform_ok sum makes any count-then-skip on a real
    entry nonconformant on the lane (P6).
  - A skip placed before `counts["entries"] += 1` keeps the sum balanced. The lane run is then
    conformant. Only selftest `got21["entries"] == 3` (for osv names) and P5's external
    `ls | wc -l` comparison catch it, not the instrument's own verdict.
- **m6. Carried and unchanged from r81:**
  - build-table.py:24 `OLD` is cwd-relative (r81 m4).
  - run_selftest merges stderr (mutbat.py:85; r81 m5).
  - The ten r80 survivors without rows (r81 m1) are still not in the table, and the claim
    does not assert them.

## Answers to the seat questions
- **New checks real?** Yes.
  - bucket-sum (:627-656) asserts both polarities of conform_ok. It also asserts the census
    sum, independently of conform_ok, and that main() consumes conform_ok: the census-swap at
    :643-649 is restored in `finally`.
  - main-default (:658-664) runs main() without `--verbose`.
  - The gaps are the m1 over-count direction and the m2 positive limb.
- **Does anything break an r81 check?** No.
  - conform_ok equals the old four-limb expression whenever the buckets balance, which is
    always true for the real census().
  - GATE_PREDICATES and GATE_ROWS=40 are unchanged.
  - The new checks have non-constant `ok` arguments (no F1), and both ids are in
    REQUIRED_CHECKS (:298-299). The docstring count is 2+7+15=24.
- **Are the transforms the routed ones?** J1, S07M, B1 and B2 are the routed or declared
  transforms (verified above). S04/S05 are re-anchored on the same conjunct.
- **Decoy and overclaim:** D1 is AST-identical on this candidate. D2 is not semantics-preserving
  in general (m3). The F8 limit is declared, but the limit is wider than AST embedding
  (Major 1).

## Residual risk / verification gaps
- Major 1 is a simulation, not a counter run.
- P1, P3 and P4 were not re-executed. The committed receipts were read (c1-forgeries-r82.txt
  lines 7-12 match P4).
- No tools were installed.
- Commands run: sha256sum, git show/diff/log/status (read-only), diff, jq, grep, sed -n,
  `python3 --version` (3.14.8), the P9 selftest, and in-process eval probes.
- Scratch `/fast/scratch/hyaku/kasegi-r82/ReviewC1` is deleted at yield.
