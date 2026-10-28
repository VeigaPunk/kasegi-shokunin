# ExecC2Counters — round 43, C2 counting commands (bundle + base transcript)

Seat: ExecC2Counters (leaf, kasegi-shokunin round 43, hyaku run 11 v2 wave)
Base: `ab98fac9dce87130bc4f66de89e30650d63943dc` (lane repo `/home/vgpnk/Projects/shokunin/kasegi-shokunin`)
Frozen claims read first: `.ufo/waves/round-43/claims.json` (C2 counting_commands). Never edited.
Control compared: `.ufo/waves/round-43/c2-controls/before.txt` (measured 2026-10-28T16:34:15Z).

## Deliverables

| file | lines | sha256 |
|---|---|---|
| `.ufo/waves/round-43/w1/ExecC2Counters.bundle.sh` | 80 | `b3b0075dc6785700254eb4c6a8913d81c3aee588cd98d8c3ea8c12ef00a08576` |
| `.ufo/waves/round-43/w1/ExecC2Counters.transcript.txt` | 14 | `17212514c443a943ab2862e7f7d40e820151d7fe98db3e030a8acacdb2f61734` |

The bundle prints one `<n>. <command> -> <value>` line per count and nothing else.
Re-run: `TMPDIR=<scratch> LANE=<lane-root> bash <this-dir>/ExecC2Counters.bundle.sh`
(or `bash <path>` from anywhere inside the lane; it resolves the repo that contains it).
It is read-only, creates no files, and exports `TMPDIR=${TMPDIR:-/tmp}` to every child.

## The ten counts, base values, and the control line each reproduces

Transcript = `17212514…` (14 lines: 3 comment header lines, ten values, one exit line).

| # | command | base value | control `before.txt` line |
|---|---|---|---|
| 1 | `grep -cE '^\|[[:space:]]*F[0-9]+[[:space:]]*\|' corpus/README.md` | `25` | (frontier census rows; control F gives the harness total `entries=28`) |
| 2 | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | `66` | `--- B. registry rows` / `66` |
| 3 | `awk -F'\|' '$2 ~ /^ *S[0-9]+ *$/ {…rows>=67…status cell…}' corpus/SOURCES.md` | `rows>=S067=0 status=absent` | `S067 onwards: 0` |
| 4 | `grep -rlE '^source: S067' corpus/knowledge \| wc -l` | `0` | `entries citing S067: 0` |
| 5 | `ls corpus/knowledge/*.md \| wc -l` | `61` | `--- C. knowledge files` / `61` |
| 6 | `python3 corpus/instruments/capture-binding-check.py` | `records=56 bound=56 unbound=0 exit=0` | `--- D. capture binding` / `records=56 bound=56 unbound=0` |
| 7 | `python3 corpus/instruments/recheck-audit.py --quiet` | `expected=61 exit=0` | `--- E. recheck audit` / `expect=present expected=61 missing=0 unexpected=0 exit=0` |
| 8 | `python3 corpus/instruments/frontier-recheck-count.py` | `entries=28 pass=28 exit=0` | `--- F. frontier harness` / `entries=28 pass=28 exit=0` |
| 9 | `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` | `exit=0` | `--- G. census` / `census-exit=0` |
| 10 | `ls corpus/instruments/fixtures/claim-package/ \| grep -c '^defect-'` | `0 dir=absent` | `--- A` / `ls: cannot access 'corpus/instruments/fixtures/claim-package'` |

Every value matches the control. **No mismatch, so no defect is charged to either side.**
Line 10 prints the numeric count plus `dir=absent`, the truthful observation at base (the
directory does not exist; a bare `0` would hide that). At Y it must print `9` with no suffix.

Two notes on the seat's naming versus `claims.json`:

- "frontier rows" is not one of the frozen `counting_commands` strings; it is the row set the
  frontier census enumerates. Counted as the `| F<n> |` table rows of `corpus/README.md`: **25
  rows** carrying **28 entry files**, which reconciles with count 8's `entries=28` (rows ≠
  entries). At Y no frontier row changes, so both values stay.
- "S067 status probe" is one awk over `corpus/SOURCES.md` that prints both the count of registry
  rows at or above S067 and the S067 row's own status cell, so it covers the control's
  `S067 onwards: 0` and the status probe in one re-runnable line. At base:
  `rows>=S067=0 status=absent`; at Y it must read `rows>=S067>=1 status=mined`.
- Count 7 parses the `expected=` token exactly (an unanchored `grep -o 'expected='` would match
  `unexpected=0` and report `expected=0`; the first draft did, and was fixed before capture).

## Base-equivalence of the run location

The base run was executed on the lane worktree, whose HEAD is the r43 freeze commit
`4cb6d4ae768481e1a14afbedc2d865a060ebacfd`, one commit above base. Proof that the counted
tree content equals `ab98fac`:

```
$ git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin diff --stat \
    ab98fac9dce87130bc4f66de89e30650d63943dc HEAD -- . ':(exclude).ufo'
<no output; 0 lines>
$ git -C … status --porcelain -- corpus SOURCES.md SCORECARD.md LOG.md corpus/lessons
<no output>
```

The freeze commit only adds `.ufo/` files, so every corpus/top-level count is the base value,
and the run happened before any C2 implementer bytes could land (no
`corpus/instruments/claim-package-check.py`, no `corpus/instruments/fixtures/claim-package/`
at run time — count 10 printed `dir=absent`).

## Independent cross-check against the ab98fac archive export

`git archive ab98fac | tar -x` into scratch, then `LANE=<export> bash bundle`:

```
1 -> 25    2 -> 66    3 -> rows>=S067=0 status=absent    4 -> 0    5 -> 61
6 -> records=56 bound=56 unbound=0 exit=0
7 -> expected=61 exit=1
8 -> entries=28 pass=28 exit=0 shell-exit=0
9 -> exit=0
10 -> 0 dir=absent
```

Nine of ten values are identical. Count 7 differs only in its exit: the recheck lines in
`corpus/knowledge/*.md` are `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && …`, and
`recheck-audit.py`'s strict `cdroot` limb requires `abspath(cd_target) == root`, so an export
root can never satisfy it. That is a structural property of the audit (it is bound to the
absolute lane path), **not** a tree difference: `expected=61`, `pass=61`, `fail-closed=24`,
`missing=0`, `unexpected=0` are identical, and the control's `exit=0` comes from the lane
checkout. The live run at the base-equivalent tree prints `exit=0`, which is the value the
control records. Counts 6, 8 and 9 likewise execute their instruments from the tree under test
and were re-run clean.

## Honesty / cleanliness checks

- No lane file outside the three wave-dir paths was written. `git status --porcelain` after all
  runs shows only the pre-existing `.ufo/waves/round-43/*` untracked wave files.
- Scratch (`/fast/scratch/hyaku/kasegi-r43/ExecC2Counters`, with `TMPDIR=$S/tmp`) removed before
  yield; `$S/tmp` was empty after the runs (the census cleans its own `mktemp` root there).
- No tool installed, no pacman, no network fetch, no git/jj mutation (read-only `log`, `diff`,
  `rev-parse`, `archive`, `status` only).
- No swarm, no subagent, no `agent://all`. One seat, one labrat (none needed).

## Risks / notes for the L1

1. The bundle must be re-run at Y to record the after values; the transcript here is the base
   run and is expected to diverge at counts 3, 4, 5, 6, 7, 10 once the C2 seats land
   (`status=mined`, `1`, `62`, `records=57 bound=57 unbound=0`, `expected=62`, `9`).
2. Because sibling seats now edit the live lane, a re-run of this bundle mid-wave reports the
   tree as it stands, not base; do not compare a mid-wave re-run against `before.txt`.
3. Counts 6, 7 and 8 (and 9, by absolute root) execute against the live lane and cannot be
   reproduced from a `git archive` export for count 7 (see above); run them in the lane.
4. `corpus/instruments/claim-package-check.py --selftest`, the exemplar and the eight `RULE`
   lines are C2 *deliverable* counts, not part of the ten this seat owns; they are absent here
   by scope.
