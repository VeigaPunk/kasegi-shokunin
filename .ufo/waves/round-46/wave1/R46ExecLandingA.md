VERDICT: DRAFT-READY

Seat R46ExecLandingA. Draft: `.ufo/waves/round-46/wave1/R46ExecLandingA.draft/r46-landing-gate.py` (stdlib python3, 20.6 KB, not installed). Nothing installed or upgraded; no tool changes. No commit/push/index mutation; the only git writes were inside scratch fixtures (every fixture git call names `-C <fixture>` after asserting `git rev-parse --show-toplevel` equals it).

## 1. Decision that needs the L1 (card rule vs the spot-check evidence)

The card rule "cited committer timestamp <= committer timestamp of the fleet commit `git log -1 -- <report>`" does NOT reproduce the round-45 defect. Measured:

```
$ git -C /home/vgpnk/Projects/shokunin log -1 --format='A=%aI C=%cI %H' a1f7761b
A=2026-10-28T19:30:06-03:00 C=2026-10-28T19:37:42-03:00 a1f7761b572e8c78d9d3b64d5d1e6a655f152a11
$ git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin log -1 --format='A=%aI C=%cI %H' 2998baa
A=2026-10-28T19:36:30-03:00 C=2026-10-28T19:36:31-03:00 2998baab4c39e6f0c1b50b150c5965e1643c4e11
```

The 19:30:06 the spot-check quotes (round-45-verifier-spotcheck.md:22) is the AUTHOR time of a1f7761; its committer time (19:37:42) is later than the lane commit (19:36:31), so a committer-vs-committer rule passes. The gate therefore prints both rules as separate checks: `date-order-committer-<h>` (the card rule, kept) and `date-order-author-<h>` (cited committer time <= author time of the same fleet commit: satisfied by a report written after the landing, impossible for one written before it, and robust to rebase/amend that rewrites committer time). The RED-BEFORE fails on the author check only; the committer check passes. If the L1 wants only the literal card rule, delete the author check, but then the round-45 defect is not closed.

## 2. RED-BEFORE receipt (real round-45 pair)

```
$ git -C /home/vgpnk/Projects/shokunin log --format='%h %cI' -- .ufo/reports/round-45/kasegi.md
a1f7761b 2026-10-28T19:37:42-03:00
$ python3 r46-landing-gate.py --post-report --lane /home/vgpnk/Projects/shokunin/kasegi-shokunin --branch master --report .ufo/reports/round-45/kasegi.md --fleet /home/vgpnk/Projects/shokunin
check shonen-heading pass=1 read=count=1
check report-committed pass=1 read=fleet=a1f7761b572e,committer=2026-10-28T19:37:42-03:00,author=2026-10-28T19:30:06-03:00
check cited-hashes pass=1 read=count=6
check resolves-2998baab pass=1 read=commit
check ancestor-2998baab pass=1 read=is-ancestor-of-master=yes
check final-tip-2998baab pass=0 read=ls-remote=323d1f5d825a,cited=2998baab4c39
check date-order-committer-2998baab pass=1 read=cited=2026-10-28T19:36:31-03:00,report-committer=2026-10-28T19:37:42-03:00
check date-order-author-2998baab pass=0 read=cited=2026-10-28T19:36:31-03:00,report-author=2026-10-28T19:30:06-03:00
check resolves-8cf62c87 pass=1 read=commit
... (5242db6f, 6662a427, 98878b73, 31068894: resolves/ancestor/date-order-committer/date-order-author all pass=1; 28 checks printed in total)
landing-gate mode=post-report checks=28 fail=2 exit=1
```

Two fails. `date-order-author-2998baab` is the spot-check defect (report authored 19:30:06, cited commit 19:36:31). `final-tip-2998baab` fails for a time-stale reason, not the defect: the lane has since moved to 323d1f5 (`git ls-remote origin refs/heads/master` and `git rev-parse master` both print 323d1f5d825a...). To isolate the defect, `--remote-tip <hash>` (historical replay only; the check's read token prints `override=` in the id's read field source, and the default path always uses ls-remote):

```
$ ... --remote-tip 2998baab4c39e6f0c1b50b150c5965e1643c4e11 | grep -v 'pass=1'
check date-order-author-2998baab pass=0 read=cited=2026-10-28T19:36:31-03:00,report-author=2026-10-28T19:30:06-03:00
landing-gate mode=post-report checks=28 fail=1 exit=1
```

Sentence scope on the real report: a line/sentence (table rows kept whole, sentences split at `. ` before a capital/backtick) matching `landed|final lane hash|lane commit`, plus every line inside a `## ...Landed...` section. That picks up line 3 (`final lane hash`, flagged final), the six Landed-changes rows (lines 24-29), and ignores the base hash `dc5bb8c6...` and 64-hex sha256 on line 3. `final` is flagged only by `final lane hash|commit|tip` / `final landed`, so line 29 ("final measurement", "landed, remote-verified") is not treated as final.

## 3. Selftest (20 cases, mutation-checked)

```
$ TMPDIR=$S python3 r46-landing-gate.py --selftest --work $S
... (20 `selftest case=...` lines, every `ok=1`; each asserts the EXACT set of failing check ids)
selftest control=always-pass agrees=4/20 control=always-fail agrees=16/20
selftest cases=20 failures=0
```

Cases: pre clean positive; dirty tree; untracked file; ahead of remote; placeholder in SCORECARD; `<LANE_HASH>`-type marker in lesson; backticked tokens in LOG (prose, passes); bare token in LOG (fails); backticked token in SCORECARD (still fails); wrong round lesson missing; post clean positive (report also cites an unrelated "Round base" hash in a non-landed sentence, ignored); unresolvable hash; non-ancestor hash (side branch); date inversion (author+committer both early); round-45 shape (author early, committer late: only `date-order-author` fails); two `## SHONEN` headings; report with no cited hash (fail); final hash not remote tip; report not committed in fleet; replay override. Do-nothing control: an always-pass gate agrees with only 4/20 case outcomes and an always-fail gate with 16/20; the selftest itself fails if either equals 20/20.

Mutation run (10 mutants of the draft made in scratch, each selftest re-run): author-order forced true -> `failures=2`; committer-order true -> 1; ancestor true -> 1; final-tip true -> 1; SHONEN `>=1` -> 1; no-hash pass -> 1; tree-clean true -> 2; remote-tip true -> 1; placeholder ignored -> 4; resolves true -> 1. 10/10 killed (every printed value is `selftest cases=20 failures=<n>` with n>=1).

## 4. Real-lane pre-report read (informational)

```
$ python3 r46-landing-gate.py --pre-report --lane /home/vgpnk/Projects/shokunin/kasegi-shokunin --branch master --round 45
check tree-clean pass=0 read=porcelain-lines=18
check jj-state pass=0 read=ahead=0,tracked=0,untracked=18
check remote-tip pass=1 read=remote=323d1f5d825a,local=323d1f5d825a
check placeholder-scorecard pass=1 read=SCORECARD.md:placeholders=0,lane-hash-markers=0
check placeholder-log pass=1 read=LOG.md:placeholders=0,lane-hash-markers=0
check placeholder-shonen pass=1 read=SHONEN.md:placeholders=0,lane-hash-markers=0
check placeholder-lesson pass=1 read=corpus/lessons/round-45.md:placeholders=0,lane-hash-markers=0
landing-gate mode=pre-report checks=7 fail=2 exit=1
```

The 18 untracked entries are the live round-46 `.ufo/waves/round-46/**` files (the lane is mid-round, not at `complete`); the gate is meant to run after the L1 has committed them.

## 5. Placeholder pattern decision

Tokens are r35-defect-closure.sh:164-165 (`filled by the L1`, `<LANE_HASH>`, grep -F). A raw count over the four files on the real lane is 4 in LOG.md and 1 in SHONEN.md (`grep -n -F -e 'filled by the L1' -e '<LANE_HASH>'`: LOG.md:1616, 1632, 1655, 1665; SHONEN.md:157), all prose describing the tokens in backticks, so a raw grep would fail every future run. SCORECARD.md and the lesson are scanned raw (D1 behavior; 0 hits on the real lane); LOG.md and SHONEN.md with inline `code spans` removed. Selftest cases pin both sides.

## 6. Limitations

- `date-order-*` uses `git log -1 -- <report>` (latest commit touching the report), per the card; a report stub committed early and later edited gets the later commit's times. A first-add variant would be stricter.
- The author-date rule trusts the author timestamp: a lane that sets `--date` can forge it. Committer time can equally be forged with env vars; nothing here defends against a lying committer.
- A placeholder wrapped in backticks inside LOG.md/SHONEN.md is not caught; only the two r35 spellings are matched (the documented r35 limit applies).
- Sentence scoping is a heuristic: a hash in a sentence without `landed|final lane hash|lane commit` outside a Landed section is not checked; short (7-12 hex) hashes are ignored per the card's 40-hex rule (round-45 report line 17 cites `3106889` short and is therefore not checked there).
- `jj-state` and `tree-clean` overlap by design; `jj-state` needs `refs/remotes/origin/<branch>` (local tracking ref) and `jj-lane.sh`; `remote-tip` is the live ls-remote (needs network if origin is remote).
- `--remote-tip` is a historical-replay switch; production runs must not pass it.
- The gate never runs a mutating git/jj command against `--lane`/`--fleet`; the selftest creates and removes its own fixtures (scratch `/fast/scratch/hyaku/kasegi-r46/R46ExecLandingA`, removed; `ls` of it prints nothing).
