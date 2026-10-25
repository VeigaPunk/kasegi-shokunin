# FixRecheckLines — C1 (depth:verifiability), round 25 wave 1

Seat: `L1Kasegi25.FixRecheckLines` (leaf). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`,
base revision `b49948f1164ef65106b2c4cbee3f53e8a44b8c41`. No VCS write, no spawn, no background job,
no tool install/upgrade performed this seat (nothing needed; `python3`/`git`/`bash` already present).

## Files changed (29, one line each, existing files only)

`corpus/knowledge/`:
`ai-assisted-finding-validation.md`, `authorization-safe-harbor-and-scope.md`, `citation-bases.md`,
`claim-anatomy-sample.md`, `claim-gates.md`, `claim-package-contract.md`,
`coordinated-disclosure-timelines.md`, `cvss-v4-severity-and-vector.md`,
`cwe-top25-2025-methodology.md`, `ev-model.md`, `evidence-dir.md`, `intake-and-finalize.md`,
`intake-surface.md`, `mission-control.md`, `mission-ledger.md`, `operator-queue.md`,
`ops-invariants.md`, `policy-access-playbook.md`, `program-quirks.md`, `repo-git-state.md`,
`retirement-autopsies.md`, `source-tree-loss-2026-09-28.md`, `submitted-registry.md`,
`target-checkouts.md`, `terminal-classes.md`, `triage-thresholds.md`, `ufo-archive-2026.md`,
`ufo-workspaces.md`, `vdp-disclosure-packages.md`.

Receipt written: `.ufo/waves/round-25/c1-after.json` (the C1 counter output).

## Transformation applied

23 lines shaped `recheck: on-restoration — <CMD> (<NOTE>)` →
`recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && <CMD>  # on-restoration — <NOTE>`
(`<CMD>` = text between `on-restoration — ` and the trailing ` (<NOTE>)`; `<NOTE>` verbatim without
its wrapping parentheses; em dash kept inside the comment; two spaces before `#`).

6 cwd-dependent lines → same command with `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && `
prefixed and nothing else changed.

The other 6 of the 35 lines were already conforming and are byte-identical (their files do not
appear in `git status`: `authorised-testing-rules-of-engagement.md`,
`cna-assignment-and-vulnerability-rules.md`, `cra-manufacturer-reporting-duties.md`,
`multiparty-vulnerability-coordination.md`, `root-loss-2026-10-12.md`,
`statutory-authorization-and-unauthorized-access.md`).

Every `test -d` / `test -d ..../.git` / `test ! -e` / `test -e` clause was retained verbatim; no
relative `corpus/...` path was converted to an absolute one (the `cd` prefix resolves them).

## Acceptance evidence (verbatim)

### (a) counter

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/recheck-audit.py --json .ufo/waves/round-25/c1-after.json | tail -1 ; echo exit=$?
lines=35 pass=35 fail-closed=23 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
exit=0
```

`exit=$?` above is `tail`'s status (pipeline). The audit process status was captured separately
(no pipe), and the instrument's own summary `exit=0` matches:

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/recheck-audit.py --json .ufo/waves/round-25/c1-after.json --quiet > /tmp/c1a.out; rc=$?; tail -1 /tmp/c1a.out; echo "audit_rc=$rc"
lines=35 pass=35 fail-closed=23 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
audit_rc=0
```

`fail-closed=23` is exactly the 23 previously parse-failing lines: every one still exits non-zero
(`lane=1 foreign=1`) and is now closed by the `test -d ~/Projects/bounties` base test rather than by
a shell syntax error. All 35 entries have `parse,cwd,paths = 1,1,1`.

### (b) diffstat

```
$ git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin diff --stat -- corpus/knowledge | tail -3
 corpus/knowledge/ufo-workspaces.md                      | 2 +-
 corpus/knowledge/vdp-disclosure-packages.md             | 2 +-
 29 files changed, 29 insertions(+), 29 deletions(-)
```

### (c) added/removed recheck counts

```
$ git -C .../kasegi-shokunin diff -U0 -- corpus/knowledge | grep -c '^+recheck:'
29
$ git -C .../kasegi-shokunin diff -U0 -- corpus/knowledge | grep -c '^-recheck:'
29
```

Spot-check of all 29 (exact, not by eye — see "Rewrite equivalence" below) found `mismatch 0`.

### (d) no non-recheck content lines

The literal command also matches the two unified-diff file headers per file (`--- i/...` / `+++ w/...`,
this repo's prefixes), so it prints 58 header lines and nothing else — a non-empty diff can never
make it print literally nothing. Filtering only the file headers, the check prints nothing:

```
$ cd .../kasegi-shokunin && git diff -- corpus/knowledge | grep -E '^[-+]' | grep -v 'recheck:' | grep -vE '^(--- |\+\+\+ )' ; echo "content_lines_exit=$?"
content_lines_exit=1
```

(`grep` exit 1 = no matching line. The unfiltered run's only matches were those `--- `/`+++ ` headers.)

### (e) anchorcheck exit unchanged

```
$ cd .../kasegi-shokunin && python3 corpus/instruments/anchorcheck.py corpus/knowledge/triage-thresholds.md
== corpus/knowledge/triage-thresholds.md: 148 in-range cite instances, 0 bad; 112 distinct anchors; LOST-RECORDED=18 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0
... (148 per-anchor OK/LOST-RECORDED lines elided) ...
anchorcheck_exit=0
```

Unchanged proven against the committed bytes, extracted read-only with `git archive HEAD` into
`/tmp/c1-head` (no VCS write):

```
$ (git -C .../kasegi-shokunin archive HEAD | tar -x -C /tmp/c1-head) ; cd /tmp/c1-head && python3 corpus/instruments/anchorcheck.py corpus/knowledge/triage-thresholds.md > /tmp/c1-head-anchor.out 2>&1; echo "head_anchorcheck_exit=$?"
head_anchorcheck_exit=0
$ cd .../kasegi-shokunin && python3 corpus/instruments/anchorcheck.py corpus/knowledge/triage-thresholds.md > /tmp/c1-wt-anchor.out 2>&1; echo "worktree_anchorcheck_exit=$?"; diff /tmp/c1-head-anchor.out /tmp/c1-wt-anchor.out > /dev/null; echo "anchorcheck_output_identical=$?"
worktree_anchorcheck_exit=0
anchorcheck_output_identical=0
```

Exit 0 before, exit 0 after, and the full anchor output (168 lines, incl. every `md:NNN` anchor
number) is byte-identical — no line numbers moved.

## Additional verification

Rewrite equivalence (parsed from `git diff -U0`, pairing each `-recheck:` with its `+recheck:`):
`on_restoration_rewrites 23 plain_prefixes 6 mismatch 0` — i.e. for all 23 the new body equals
`<CMD>  # on-restoration — <NOTE>` exactly, and for all 6 the new body equals the old body exactly.

Shape of the 29 new lines: `prefixed 29`, `on_restoration_shaped 23`, `comment_shape_bad 0`,
`single_line_all True`.

Line counts / R6: `git diff --numstat -- corpus/knowledge` is `1 1` for every one of the 29 files
(29 files, no file with an insertion/deletion imbalance) → no line added, dropped or moved.

Worktree scope: `git status --porcelain -- corpus/knowledge | wc -l` = `29`, all ` M`, no untracked,
no other path touched.

Fail-closed reason, before vs after: before, the 23 had `lane=2 foreign=2` (bash syntax error on the
prose hybrid); after, `lane=1 foreign=1`, and the closing test is the one the note names —
`~/Projects/bounties`, `~/Projects/the-bounty-hunter`, `~/Projects/origin-work` are all absent:

```
$ ls -d ~/Projects/bounties ~/Projects/the-bounty-hunter ~/Projects/origin-work
ls: cannot access '/home/vgpnk/Projects/bounties': No such file or directory
ls: cannot access '/home/vgpnk/Projects/the-bounty-hunter': No such file or directory
ls: cannot access '/home/vgpnk/Projects/origin-work': No such file or directory
(exit 2)
```

## Risks / notes for the L1

- Acceptance (d) as literally written cannot print nothing for a non-empty diff, because `grep -E '^[-+]'`
  matches the `--- ` / `+++ ` file headers; the header-filtered form is empty (exit 1). Recorded
  verbatim rather than massaged.
- The 23 fail-closed lines now exit 1 instead of 2. Count preserved (23), closed-ness preserved, and
  the closing cause is now the documented absent base instead of an accidental syntax error. If the
  claim's `do_nothing_control`/`kill_rule` reader compares exit codes rather than the `fail-closed`
  class, this is the one number that moved; `c1-after.json` records it per entry.
- `c1-after.json` was written by this seat at the path the counter names.
