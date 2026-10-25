# C1SemanticsAudit — round 25 wave 2 (falsification of C1 receipts)

Seat: `L1Kasegi25.C1SemanticsAudit`. Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Scope: re-check the 37 entry `recheck:` lines; classify executes/gated/broken; verify no
fail-closed test was removed (kill-rule limb). Read-only; no production edits, no VCS writes,
no spawns. Tool installs/updates: none (used preinstalled `python3`, `git`, `bash`, `diff`).
Pacman untouched.

## Verdict

**WAVE-1 RESULT HOLDS.** The 37-line final-tree receipt, the 35-line frozen-surface receipt,
and the 35-line before receipt all reproduce byte-for-byte under the committed instrument
(`sha256=c3c19adc…`), and the kill-rule limb is clean: **0 of 34 fail-closed `test` clauses
were removed, moved into comments, or added.** One per-entry `lane_output_sha256` in the
*before* receipt no longer reproduces (environmental, see Findings) — it does not change any
verdict, count, or classification.

## Commands, output, exit (verbatim)

Environment: HEAD = `b49948f1164ef65106b2c4cbee3f53e8a44b8c41` = claim `base_revision`;
wave-1 work is uncommitted (`git status --porcelain` = 44 paths, 29 ` M` under
`corpus/knowledge/`, 2 `??` new knowledge files, plus docs/.ufo).

### 1. Instrument identity

```
$ sha256sum corpus/instruments/recheck-audit.py
c3c19adcde927ac83460ad5a9855b5178935c1f5b8ec41291e8a4fd0ba2f6d7f  corpus/instruments/recheck-audit.py
$ python3 corpus/instruments/recheck-audit.py --selftest; echo exit=$?
selftest cases=14 failures=0 exit=0        (all 13 per-case want/got rows ok)
exit=0
```

Matches `c1-instrument-digest.txt` / receipt index line 3-4.

### 2. Final tree (37 lines) — matches `c1-after.json` / `c1-after.txt`

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && \
  python3 corpus/instruments/recheck-audit.py --json /tmp/c1-w2-final.json > /tmp/c1-w2-final.txt; echo rc=$?
strict pass=37/37 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=14 gated=23 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
lines=37 total=37 pass=37 fail-closed=23 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
rc=0
```

Per-entry diff vs `.ufo/waves/round-25/c1-after.json`: **0 mismatches across 37 entries** on
`command, class, lane_exit, foreign_exit, pass, pass_strict, lane_output_sha256,
foreign_output_sha256, missing_paths, limbs, strict` (python set-compare, artifact
`/tmp/c1-w2-final.json`).

### 3. Frozen surface (35 lines) — matches `c1-after-35.json`

```
$ python3 corpus/instruments/recheck-audit.py --root .ufo/waves/round-25/c1-after-35 \
  --cdroot /home/vgpnk/Projects/shokunin/kasegi-shokunin --json /tmp/c1-w2-frozen35.json; echo rc=$?
strict pass=35/35 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=12 gated=23 broken=0
lines=35 total=35 pass=35 fail-closed=23 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
rc=0
```

### 4. Before (do-nothing control) — HEAD bytes extracted read-only

```
$ rm -rf /tmp/c1-head-w2 && mkdir -p /tmp/c1-head-w2 && \
  git archive HEAD corpus | tar -x -C /tmp/c1-head-w2 && \
  python3 corpus/instruments/recheck-audit.py --root /tmp/c1-head-w2 \
  --cdroot /home/vgpnk/Projects/shokunin/kasegi-shokunin --json /tmp/c1-w2-before.json; echo rc=$?
strict pass=6/35 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=12 gated=0 broken=23
lines=35 total=35 pass=6 fail-closed=23 parse_fail=23 cwd_fail=6 paths_fail=0 exit=1
rc=1
```

Reproduces `c1-before-strict.*` and the claim's `before`/`do_nothing_control`
(`pass=6 exit=1`; 23 prose+command hybrids, 6 cwd-dependent with lane=0/foreign=2 — verified
per entry). Wave-1's own `c1-controls/base/corpus/knowledge` tree is byte-identical to HEAD
bytes: `diff -r -q` over all 35 files, `file_diff=0`.

### 5. Kill rule: no fail-closed test removed

Every `test -[def]`/`test ! -e` clause in each HEAD `recheck:` line must survive verbatim in
the worktree line's executable part. Multiset check over all 35 tracked files:

```
files checked: 35
files with old test clauses: 24     (23 gated lines + root-loss-2026-10-12.md)
total old test clauses: 34
missing old clauses: 0
added new clauses: 0
total test clauses in code part across 37 worktree lines: 34
clauses stranded in comments: 0
```

So the 23 on-restoration rewrites kept every closing test **before** the `  #` comment
boundary; `root-loss-2026-10-12.md`'s four `test ! -e`/`test -e` assertions are unchanged;
the two new files carry no test clauses (they recheck `corpus/source-snapshots/round-25/
manifest.json`, which exists).

### 6. Gate conditions are real

```
$ ls -d ~/Projects/bounties ~/Projects/the-bounty-hunter ~/Projects/origin-work
ls: cannot access ... (all three)   exit=2
$ ls -d ~/Projects/ufo-fsd-alpha
/home/vgpnk/Projects/ufo-fsd-alpha   exit=0
```

All 23 gated entries exit `lane=1 foreign=1` (uniform set `{1}`), digest-equal under cwd —
i.e. they *run* and fail closed on the absent bases they name, not on syntax. The 14
executes include `root-loss-2026-10-12.md`, which correctly exits 0 only because
`ufo-fsd-alpha` is present while the three named bases are absent.

## Classification (current tree, independently recomputed)

- **executes (14):** ai-assisted-finding-validation, authorised-testing-rules-of-engagement,
  authorization-safe-harbor-and-scope, citation-bases, cna-assignment-and-vulnerability-rules,
  coordinated-disclosure-timelines, cra-manufacturer-reporting-duties,
  cvss-v4-severity-and-vector, cwe-top25-2025-methodology, multiparty-vulnerability-coordination,
  root-loss-2026-10-12, statutory-authorization-and-unauthorized-access,
  vendor-disclosure-policies-as-corpus-objects, vendor-disclosure-policy-commitments-crosswalk.
- **gated (23):** claim-anatomy-sample, claim-gates, claim-package-contract, ev-model,
  evidence-dir, intake-and-finalize, intake-surface, mission-control, mission-ledger,
  operator-queue, ops-invariants, policy-access-playbook, program-quirks, repo-git-state,
  retirement-autopsies, source-tree-loss-2026-09-28, submitted-registry, target-checkouts,
  terminal-classes, triage-thresholds, ufo-archive-2026, ufo-workspaces, vdp-disclosure-packages.
- **broken (0).**

## Findings

1. **[low, informational] Before-receipt digest not frozen-reproducible:**
   `c1-before-strict.json`'s `citation-bases.md.lane_output_sha256`
   (`87f1f6e0…`) differs from today's HEAD-bytes run (`0217f6b0…`). Cause: the
   `anchorcheck.py` base mirror `~/Projects/the-bounty-hunter` was present during the wave-1
   capture (its `c1-controls/base` run reports `BASE-ABSENT=1`, `OK md:13/md:16/…`) and is
   absent now (`BASE-ABSENT=9`). The input file is byte-identical (`diff` clean), the
   instrument is the same sha, and the limb/class/verdict outcomes are unchanged
   (`pass=False`, `cwd` fails either way because foreign `/` never had the mirror). It only
   means before-receipt output digests are environment-dependent artifacts, not that the
   receipt was falsified. Residual risk: any future re-derivation of `c1-before-strict.json`
   must re-anchor digests rather than diff them.
2. **No actionable defect.** Executed/gated/broken counts, all three surface totals, the
   do-nothing control, and the kill-rule limb all reproduce. The claim C1 stands: frozen
   35/35, final tree 37/37, fail-closed count preserved at 23 with every closing test intact.

## Smallest correction if held against receipts

None required for the claim. Optional annotation only: note in `c1-receipt-index.txt` that
`c1-before-strict`'s per-entry output digests for `anchorcheck`-invoking lines
(`citation-bases.md` observed) are mirror-state-dependent and will drift now that
`~/Projects/the-bounty-hunter` is absent.
