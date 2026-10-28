VERDICT: DRAFT-READY

Seat R46ExecLandingB, mistake-fix builder B. Draft: `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-46/wave1/R46ExecLandingB.draft/r46-landing-gate.py` (python3 stdlib, 26.9 kB, mode 0755). It is not installed, not committed. I read no sibling draft. The only git/jj commands I ran against the lane and fleet were read-only. The only mutating git calls were on fixtures under my scratch, each guarded by a `rev-parse --show-toplevel` equality assert.

Tooling installed: none.

## 0. Decision the L1 must see: the specified date check passes on the real round-45 pair

The task asks for the committer timestamp of the cited hash `<=` the committer timestamp of the fleet commit that adds the report, and says the real round-45 replay must exit 1 on that check. Measured, the committer-vs-committer reading is not the defect:

```
$ git -C /home/vgpnk/Projects/shokunin log --format='%h an=%an ad=%aI cd=%cI' -- .ufo/reports/round-45/kasegi.md
a1f7761b an=kasegi-shokunin ad=2026-10-28T19:30:06-03:00 cd=2026-10-28T19:37:42-03:00
$ git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin log -1 --format='%h ad=%aI cd=%cI' 2998baa
2998baa ad=2026-10-28T19:36:30-03:00 cd=2026-10-28T19:36:31-03:00
```

- The spot-check's "19:30:06" is the report commit's AUTHOR date. Its committer date is 19:37:42, which is after 2998baa's 19:36:31, so committer-vs-committer is satisfied.
- The commit was rewritten after authoring (author date 7 min 36 s before committer date), which is exactly what moves the committer clock later.
- A committer-only gate would therefore have passed the defect.

So the gate prints two checks:

- `date-order`: the specified check, committer vs committer.
- `date-order-author`: cited committer time `<=` the report commit's AUTHOR time, the clock the defect inverted.

Mutant M1 below (author check reading the committer clock instead) shows the selftest catches this degradation.

## 1. RED-BEFORE receipt (real round-45 pair, run by me)

Command A (literal, live ls-remote):

```
$ python3 r46-landing-gate.py --post-report --lane /home/vgpnk/Projects/shokunin/kasegi-shokunin --branch master --report .ufo/reports/round-45/kasegi.md --fleet /home/vgpnk/Projects/shokunin
check report-readable pass=1 read=bytes=15428
check cited-hashes pass=1 read=n=6,final=1
check resolves pass=1 read=unresolved=0
check ancestor pass=1 read=non-ancestor=0
check final-is-tip pass=0 read=final-not-tip=2998baab4c39,tip=323d1f5d825a(ls-remote)
check date-order pass=1 read=latest-cited=2998baab4c39@2026-10-28T19:36:31-03:00,report-commit-committer=2026-10-28T19:37:42-03:00
check date-order-author pass=0 read=latest-cited=2998baab4c39@2026-10-28T19:36:31-03:00,report-commit-author=2026-10-28T19:30:06-03:00
check shonen-heading pass=1 read=count=1
landing-gate mode=post-report checks=8 fail=2 exit=1
```

Command B: the same run with `--tip 2998baab4c39e6f0c1b50b150c5965e1643c4e11` (replay override, printed as `(override)`). It isolates the spot-check's reason, because the lane has since advanced to `323d1f5`, so run A also fails `final-is-tip` honestly:

```
check final-is-tip pass=1 read=final-not-tip=0,tip=2998baab4c39(override)
check date-order pass=1 read=latest-cited=2998baab4c39@2026-10-28T19:36:31-03:00,report-commit-committer=2026-10-28T19:37:42-03:00
check date-order-author pass=0 read=latest-cited=2998baab4c39@2026-10-28T19:36:31-03:00,report-commit-author=2026-10-28T19:30:06-03:00
landing-gate mode=post-report checks=8 fail=1 exit=1
```

The other six checks pass and are printed in full (report-readable, cited-hashes, resolves, ancestor, final-is-tip, shonen-heading). The one failure is `date-order-author`, for the spot-check's reason: the report authored 19:30:06 cites `2998baab…` committed 19:36:31. The extractor found 6 cited hashes, 1 final: `2998baab…` final, plus `8cf62c8`, `5242db6`, `6662a42`, `98878b7` and `3106889` from the Commit column of the Landed-changes table.

`git -C /home/vgpnk/Projects/shokunin log --format='%h %cI' -- .ufo/reports/round-45/kasegi.md` printed `a1f7761b 2026-10-28T19:37:42-03:00`.

## 2. Selftest (my run, 30 cases, 0 failures)

```
$ TMPDIR=$S python3 r46-landing-gate.py --selftest --work $S
selftest case=readonly-guard-refuses-commit expect=refuse got=refuse verdict=pass
selftest case=pre-clean-positive expect=- got=- verdict=pass
selftest case=pre-dirty-tracked-file expect=jj-state,tree-clean got=jj-state,tree-clean verdict=pass
selftest case=pre-untracked-file expect=jj-state,tree-clean got=jj-state,tree-clean verdict=pass
selftest case=pre-ahead-of-remote expect=jj-state,remote-tip got=jj-state,remote-tip verdict=pass
selftest case=pre-remote-moved-by-other-writer expect=remote-tip got=remote-tip verdict=pass
selftest case=pre-placeholder-filled-by-L1-scorecard … got=placeholders verdict=pass
selftest case=pre-placeholder-lane-hash-log-bare … got=placeholders verdict=pass
selftest case=pre-placeholder-lane-hash-lesson … got=placeholders verdict=pass
selftest case=pre-backticked-quote-in-log-exempt expect=- got=- verdict=pass
selftest case=pre-backticked-quote-in-scorecard-strict … got=placeholders verdict=pass
selftest case=pre-round-lesson-missing … got=placeholders verdict=pass
selftest case=pre-do-nothing-control-no-lane expect=jj-state,placeholders,remote-tip,tree-clean got=<same> verdict=pass
selftest case=post-clean-positive expect=- got=- verdict=pass
selftest case=post-report-with-no-cited-hash expect=ancestor,cited-hashes,date-order,date-order-author,final-is-tip,resolves got=<same> verdict=pass
selftest case=post-unresolvable-hash expect=ancestor,date-order,date-order-author,resolves got=<same> verdict=pass
selftest case=post-non-ancestor-hash expect=ancestor got=ancestor verdict=pass
selftest case=post-table-commit-column-non-ancestor expect=ancestor got=ancestor verdict=pass
selftest case=post-date-inversion-committer-and-author expect=date-order,date-order-author got=<same> verdict=pass
selftest case=post-date-inversion-author-only-round45-shape expect=date-order-author got=date-order-author verdict=pass
selftest case=post-two-shonen-headings expect=shonen-heading got=shonen-heading verdict=pass
selftest case=post-zero-shonen-headings expect=shonen-heading got=shonen-heading verdict=pass
selftest case=post-final-hash-not-tip expect=final-is-tip got=final-is-tip verdict=pass
selftest case=post-no-final-sentence-fails-closed expect=final-is-tip got=final-is-tip verdict=pass
selftest case=post-report-untracked-in-fleet expect=date-order,date-order-author got=<same> verdict=pass
selftest case=post-tip-moved-after-report-live-tip expect=final-is-tip got=final-is-tip verdict=pass
selftest case=post-tip-moved-after-report-replay-override expect=- got=- verdict=pass
selftest case=post-do-nothing-control-missing-report expect=<all 8 post checks> got=<same> verdict=pass
selftest case=cli-positive exit=0 last=landing-gate_mode=post-report_checks=8_fail=0_exit=0 verdict=pass
selftest case=cli-two-shonen exit=1 last=landing-gate_mode=post-report_checks=8_fail=1_exit=1 verdict=pass
selftest cases=30 failures=0
```

(`…` and `<same>` abbreviate lines that printed in full; every verdict was `pass`.) The cases the task named are all present:

| Required case | Selftest case |
|---|---|
| dirty tree | `pre-dirty-tracked-file` |
| untracked file | `pre-untracked-file` |
| ahead of remote | `pre-ahead-of-remote` |
| placeholder token | the three `pre-placeholder-…` cases |
| unresolvable hash | `post-unresolvable-hash` |
| non-ancestor hash | `post-non-ancestor-hash` |
| date inversion | `post-date-inversion-committer-and-author` and `…-author-only-round45-shape` |
| two SHONEN headings | `post-two-shonen-headings` |
| clean positive | `pre-clean-positive`, `post-clean-positive` |
| no cited hash = fail | `post-report-with-no-cited-hash` |

## 3. Mutants (do-nothing discrimination, my run)

Seven one-line mutants of a scratch copy, each run through `--selftest`. All seven exit 1, so the cases are not vacuous:

```
M1-author-uses-committer    exit=1 selftest cases=30 failures=1 ['…post-date-inversion-author-only-round45-shape']
M2-no-backtick-exemption    exit=1 selftest cases=30 failures=1 ['…pre-backticked-quote-in-log-exempt']
M3-ancestor-always-ok       exit=1 selftest cases=30 failures=3 [unresolvable, non-ancestor, table non-ancestor]
M4-remote-tip-self          exit=1 selftest cases=30 failures=2 [pre-ahead-of-remote, pre-remote-moved-by-other-writer]
M5-no-final-vacuous         exit=1 selftest cases=30 failures=3 [no-cited-hash, no-final-sentence, missing-report]
M6-shonen-ge1               exit=1 selftest cases=30 failures=2 [two-shonen, cli-two-shonen]
M7-untracked-ignored-jj     exit=1 selftest cases=30 failures=1 [pre-untracked-file]
```

M1 is the specified committer-only gate and it fails on the round-45 shape, which is the do-nothing control for section 0. The case `pre-remote-moved-by-other-writer` shows `ls-remote` catches what `jj-lane.sh state` cannot: state reads the stale local `refs/remotes/origin/master` and reports `ahead=0`.

## 4. Pre-report on the real lane (informational, mid-wave)

```
$ python3 r46-landing-gate.py --pre-report --lane /home/vgpnk/Projects/shokunin/kasegi-shokunin --branch master --round 45
check tree-clean pass=0 read=porcelain-lines=29
check jj-state pass=0 read=ahead=0,tracked=0,untracked=29
check remote-tip pass=1 read=remote=323d1f5d825a,local=323d1f5d825a
check placeholders pass=1 read=SCORECARD.md=0,LOG.md=0,SHONEN.md=0,corpus/lessons/round-45.md=0
landing-gate mode=pre-report checks=4 fail=2 exit=1
```

The 29 untracked paths are this wave's uncommitted drafts and reports, so it exits 1 as it should. With `--round 46` the placeholder check reads `corpus/lessons/round-46.md=missing` and fails, since that lesson does not exist yet.

## 5. Design choices beyond the spec (all fail-closed, all disclosed)

- **Placeholder tokens:** exactly the two D1 literals, `filled by the L1` and `<LANE_HASH>`. They are spelled split in the source so the file never matches its own grep.
  - SCORECARD.md is strict, the same plain count as r35 D1.
  - LOG.md, SHONEN.md and the round lesson ignore a token inside an inline backtick span. On the real tree LOG.md has 2 and 2 and SHONEN.md has 1 quoted occurrences (`LOG.md:1616`, `:1632`, `SHONEN.md:157`), and strict counting would red-flag history.
  - Hole, stated: a placeholder written inside backticks in LOG.md, SHONEN.md or the lesson escapes. The prose spelling "the L1 fills this line" stays uncovered, as r35 D1 itself documents.
- **Cited-hash extraction:** a sentence containing `landed`, `final lane hash` or `lane commit`, or a table cell under a `Commit`/`Hash` header. Paragraphs are re-joined across wrapped lines before sentence splitting. Only 40-hex hashes count, so short hashes are not checked.
- **Final-sentence rule:** `final-is-tip` also fails when no sentence says `final` (`final-sentences=0`), because otherwise a report that never names its final hash would pass.
- **Zero cited hashes:** `cited-hashes` fails and every dependent check fails with `no-cited-hashes`; none passes vacuously.
- **Extra checks:** `report-readable` and `date-order-author` are not in the spec.
- **Fleet add commit:** found with `git log --diff-filter=A` (oldest add). A report never added in the fleet fails both date checks (`report-not-added-in-fleet`).
- **Replay flag:** `--tip REV` is opt-in and printed as `(override)`. Without it the live `ls-remote` is used.
- **Read-only guard:** `git()` allows only status, rev-parse, ls-remote, log, merge-base, cat-file, show and rev-list, and passes `--no-optional-locks`. Selftest asserts that `commit` is refused. `fx()` (the fixture-only mutator) is never reachable from the gate modes.

## 6. Limitations

- `final-is-tip` replay against a past report fails once the lane advances (run A). Use `--tip` for replays only.
- `jj-lane.sh state` itself runs `git status` without `--no-optional-locks`, so the pre-report mode touches the lane index through that helper, as the spec required.
- The report is read from the fleet working tree, not from the committed blob; a later uncommitted edit to the report is not detected.
- `--pre-report` and `--post-report` need network for `ls-remote origin`. A network failure reads as `remote=none` and fails closed.
- The fixture `origin` is a local bare repo, so the real GitHub transport was exercised only by the live runs in sections 1 and 4, and only for `ls-remote`.
- The gate proves ordering and quiescence at the moment it runs; it cannot stop a later commit moving the tip.
- Not run: any other seat's gate, the F28 entry and the C1 re-grounds (assigned elsewhere). This draft is the only deliverable of this seat.

Scratch `/fast/scratch/hyaku/kasegi-r46/R46ExecLandingB` removed on exit.
