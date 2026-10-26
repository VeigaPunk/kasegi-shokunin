# ExecScoreGap — round 39 — distance-to-next-score measurement (proposal 1 mining)

Seat: ExecScoreGap (leaf). Axis: depth:verifiability. Milestone: round-39.
Lane: /home/vgpnk/Projects/shokunin/kasegi-shokunin (base 480b1a505a2dfc14a4f718d16d63808247214d0a,
claims freeze dcd31701720a6a4929a32471a62011ed87103421, worktree HEAD d65d823e7c84813c192b20ee757a8761f878a61f).
Scratch: /fast/scratch/hyaku/kasegi-r39/ExecScoreGap (removed at exit). No git/jj mutation anywhere.
No tool installed or upgraded this seat (no pacman, no uv, no npx, no binary fetch).

Deliverable: `.ufo/waves/round-39/wave1/ExecScoreGap.gap.txt` — 167 lines,
sha256 `65f5e7b1eb91bcec11e441137ebb03b8d2ccb14dee31af0d0bc6d97db1908e5d`.
It carries the verbatim instrument output (score-gap report, full recheck-audit listing), the
counts, and the gated-entry decomposition. Nothing in it is landable prose; it is measurement.

## Base equivalence (why the worktree is "at base")

```
$ git -C <lane> diff --stat 480b1a505a2dfc14a4f718d16d63808247214d0a..HEAD -- .
 .ufo/waves/round-39/{build-wave1-final.py,build-wave1-spec.py,c1-controls/before.txt,
 c2-controls/before.txt,c2-controls/junk-f22.md,census-before.txt,claims.json,items1.py,
 wave1-dispatch.json,wave1-plan.out,wave1-spec.json}
 11 files changed, 2366 insertions(+)
```
Only `.ufo/waves/round-39/*` differs from base, so `corpus/`, `SKILL.md`, `SCORECARD.md` in this
worktree are byte-identical to base. `git diff-index --quiet HEAD --` → clean before and after the run.

## Commands actually run (cwd = lane, TMPDIR = scratch)

```
$ python3 corpus/instruments/score-gap.py                          # exit 0
$ python3 corpus/instruments/recheck-audit.py --root .             # exit 0 (full, not --quiet)
$ python3 corpus/instruments/frontier-recheck-count.py             # exit 0
$ python3 corpus/instruments/anchorcheck.py corpus/knowledge/citation-bases.md   # exit 1 (see §Gated)
$ python3 corpus/instruments/score-gap.py --selftest                # exit 0
$ python3 corpus/instruments/recheck-audit.py --selftest            # exit 0
$ grep -cE '^\| F[0-9]+ \|' corpus/README.md                        # 21
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md   # 55
$ ls corpus/knowledge/*.md | wc -l                                  # 50
$ grep -l '^recheck:' corpus/knowledge/*.md | wc -l                 # 50
```
Instrument identity: `score-gap.py` sha256 `57584fda83b813e44fb2e2cb6cb2b1e4af1dd20f07877a6b119db9ba9feb43cf`,
`recheck-audit.py` sha256 `5d4842da6103f17c7798ca2078a77288820bd8b90432348cd2cc012e1faf7f09` (both also
printed by score-gap's own `source:` lines).

## Measured breakdown at base

| field | value |
|---|---|
| strict pass | **50/50** (`cdroot_fail=0 instrument_fail=0 own_fail=0`) |
| class split | `executes=26 gated=24 broken=0` |
| line/governance line | `lines=50 total=50 pass=50 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0` |
| expect line | `expect=present expected=50 missing=0 unexpected=0 exit=0` |
| gated-unsupported-claims count | **24** (score-gap field 5: `gap: 24 of 50 rechecks still gated on a lost base; score 5 needs 0 gated unsupported claims`) |
| anchorcheck (SKILL.md) | `in-range=16 bad=0 lost-recorded=306 origin=0 outside-base=0 base-absent=0 exit=0` |
| census (committed figures) | lane `134/1480 = 9.05%`, SKILL.md `32/506 = 6.32%` |
| score-5 threshold | `SCORECARD.md:331 "Threshold for 5: a non-author audit passing 25/25 source chains and 0 unsupported current claims."` (1 match) |
| frontier rows | **21** (max F21) |
| registry rows (S###) | **55** (max S055) |
| knowledge entries | **50** |
| source chains | `entries=24 pass=24 exit=0` |

Every entry is `PASS` on both limb sets (`frozen=111 strict=111111`); no `FAIL`, no `FROZEN-ONLY`.

## Gated-entry decomposition (the number proposal 1 mines)

`gated=24` is not one blocker. Per-entry, strip the `test -d <base> &&` guard and re-run the rest:

- **23 of 24** are gated on an absent external base; of those **22 go green the day the base returns**
  (`post_strip_exit=0`). The 23rd, `repo-git-state.md`, still exits 128 because it needs a real
  `git -C ~/Projects/bounties rev-parse HEAD` repo, not a restored directory skeleton.
- **1 of 24** (`citation-bases.md`) is gated on a lost-tree record, not a base:
  `anchorcheck.py corpus/knowledge/citation-bases.md` exits 1 on
  `LOST-RECORDED md:52 [lost-tree] ops/claim-check.mjs:174-199 (not checked)`.
- Distinct blockers: `~/Projects/bounties` 22 entries, `~/Projects/the-bounty-hunter` 6,
  `~/Projects/bounties/.git` 1, `~/Projects/origin-work` 1 (bases absent since 2026-09-28 / 2026-10-12;
  verified absent on host this session).

So the live distance to score 5 is two legs: the chain leg reads **24/25** (F22/S057 closes it this
round) and the unsupported-claims leg reads **24 gated / needs 0**, and **no lane edit moves the
second leg** — all 24 depend on state outside the lane. That is the explicit distance figure for
proposal 1, and it is the same number before and after any round-39 in-lane work.

## Observation (recorded, not changed — out of seat write scope)

`score-gap.py` field 5 and `recheck-audit.py`'s printed gloss both describe `gated` as
"gated on a lost base / fails closed on an absent base". At base that phrase over-covers by exactly
one entry (`citation-bases.md`, gated on a lost anchor). The count `gated=24` is correct; only the
cause gloss is 1 too broad. Instruments are outside this seat's write scope, so nothing was edited;
flagging for the L1 in case a later instrument pass wants the gloss split (absent-base vs lost-anchor).

## Instrument selftests (both green, so the numbers come from self-tested instruments)

```
$ python3 corpus/instruments/score-gap.py --selftest
selftest recheck-mode=real
selftest exit-a  ok rc=0 want=0 ...
selftest no-write-a  ok tree digest unchanged=True
selftest fields=7 failures=0                          # exit 0
$ python3 corpus/instruments/recheck-audit.py --selftest
18 selftest lines, 0 FAIL                             # exit 0
```

## Risks / blockers

None. The worktree tracked tree is clean after the run; no writes outside the two allowed wave1
paths and scratch; scratch dir and `/tmp/cite.out` removed before yield.
