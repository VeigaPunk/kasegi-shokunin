VERDICT: BROKEN

Scope: landing gate `corpus/instruments/r46-landing-gate.py` at lane commit 5437afeaf9b642c267bba3c31f00ae701e49da68 (the frozen integrated tree). Lane HEAD is 0d121a2, one spec-only commit later; the gate blob is identical at both (`bbef9109148e17eaf6b36220f386fde283934fc6`). Nothing in the lane was edited, committed or staged.

## Setup and baseline (re-run)

- Export: `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive 5437afeaf9b642c267bba3c31f00ae701e49da68 | tar -x -C /fast/scratch/hyaku/kasegi-r46/R46W2MutLanding/export`
- Identity: `export-sha=7ad171e73b1b211d0fd6b8616157ffd085b4f17468a415b842ffe01ddaba8fc4` and `worktree-sha=7ad171e73b1b211d0fd6b8616157ffd085b4f17468a415b842ffe01ddaba8fc4`; 637 lines.
- Unmodified control: `python3 base.py --selftest --work .../work/base` printed
  `selftest cases=30 failures=0` (exit 0). Gate's own `readonly-guard-refuses-commit` case passed.

## Finding 1: mutation battery (23 single-line mutants + 2 do-nothing controls)

Driver: `mutate.py` applied one `str.replace` per mutant to a copy of the frozen export (each anchor asserted to occur exactly once), then ran `<mutant> --selftest --work <dir>`. Verbatim driver output:

```
mutant=tree-clean-flip selftest-failures=11 rejected=1 cases=30 rc=1 failing-cases=pre-clean-positive,pre-dirty-tracked-file,pre-untracked-file,pre-ahead-of-remote,pre-remote-moved-by-other-writer,pre-placeholder-filled-by-L1-scorecard,pre-placeholder-lane-hash-log-bare,pre-placeholder-lane-hash-lesson,pre-backticked-quote-in-log-exempt,pre-backticked-quote-in-scorecard-strict,pre-round-lesson-missing
mutant=tree-ignores-untracked selftest-failures=1 rejected=1 cases=30 rc=1 failing-cases=pre-untracked-file
mutant=jj-ignores-untracked selftest-failures=1 rejected=1 cases=30 rc=1 failing-cases=pre-untracked-file
mutant=jj-accepts-ahead selftest-failures=1 rejected=1 cases=30 rc=1 failing-cases=pre-ahead-of-remote
mutant=jj-flip-ahead selftest-failures=9 rejected=1 cases=30 rc=1 failing-cases=pre-clean-positive,pre-ahead-of-remote,pre-remote-moved-by-other-writer,pre-placeholder-filled-by-L1-scorecard,pre-placeholder-lane-hash-log-bare,pre-placeholder-lane-hash-lesson,pre-backticked-quote-in-log-exempt,pre-backticked-quote-in-scorecard-strict,pre-round-lesson-missing
mutant=remote-skip-ls-remote-compare selftest-failures=2 rejected=1 cases=30 rc=1 failing-cases=pre-ahead-of-remote,pre-remote-moved-by-other-writer
mutant=remote-flip-compare selftest-failures=11 rejected=1 cases=30 rc=1 failing-cases=pre-clean-positive,pre-dirty-tracked-file,pre-untracked-file,pre-ahead-of-remote,pre-remote-moved-by-other-writer,pre-placeholder-filled-by-L1-scorecard,pre-placeholder-lane-hash-log-bare,pre-placeholder-lane-hash-lesson,pre-backticked-quote-in-log-exempt,pre-backticked-quote-in-scorecard-strict,pre-round-lesson-missing
mutant=ancestor-dropped selftest-failures=2 rejected=1 cases=30 rc=1 failing-cases=post-non-ancestor-hash,post-table-commit-column-non-ancestor
mutant=ancestor-flip selftest-failures=12 rejected=1 cases=30 rc=1 failing-cases=post-clean-positive,post-date-inversion-committer-and-author,post-date-inversion-author-only-round45-shape,post-two-shonen-headings,post-zero-shonen-headings,post-final-hash-not-tip,post-no-final-sentence-fails-closed,post-report-untracked-in-fleet,post-tip-moved-after-report-live-tip,post-tip-moved-after-report-replay-override,cli-positive,cli-two-shonen
mutant=accept-abbreviated-hashes selftest-failures=0 rejected=0 cases=30 rc=0 failing-cases=-
mutant=author-time-as-committer selftest-failures=1 rejected=1 cases=30 rc=1 failing-cases=post-date-inversion-author-only-round45-shape
mutant=date-strict-boundary selftest-failures=0 rejected=0 cases=30 rc=0 failing-cases=-
mutant=date-ignores-unreadable selftest-failures=1 rejected=1 cases=30 rc=1 failing-cases=post-unresolvable-hash
mutant=author-check-reads-committer selftest-failures=1 rejected=1 cases=30 rc=1 failing-cases=post-date-inversion-author-only-round45-shape
mutant=final-tip-compare-dropped selftest-failures=2 rejected=1 cases=30 rc=1 failing-cases=post-final-hash-not-tip,post-tip-moved-after-report-live-tip
mutant=final-flag-never-set selftest-failures=12 rejected=1 cases=30 rc=1 failing-cases=post-clean-positive,post-unresolvable-hash,post-non-ancestor-hash,post-table-commit-column-non-ancestor,post-date-inversion-committer-and-author,post-date-inversion-author-only-round45-shape,post-two-shonen-headings,post-zero-shonen-headings,post-report-untracked-in-fleet,post-tip-moved-after-report-replay-override,cli-positive,cli-two-shonen
mutant=shonen-at-least-one selftest-failures=2 rejected=1 cases=30 rc=1 failing-cases=post-two-shonen-headings,cli-two-shonen
mutant=cited-hashes-zero-ok selftest-failures=2 rejected=1 cases=30 rc=1 failing-cases=post-report-with-no-cited-hash,post-do-nothing-control-missing-report
mutant=placeholders-backtick-exempt-everywhere selftest-failures=1 rejected=1 cases=30 rc=1 failing-cases=pre-backticked-quote-in-scorecard-strict
mutant=placeholder-missing-file-passes selftest-failures=2 rejected=1 cases=30 rc=1 failing-cases=pre-round-lesson-missing,pre-do-nothing-control-no-lane
mutant=resolves-passes-without-cites selftest-failures=2 rejected=1 cases=30 rc=1 failing-cases=post-report-with-no-cited-hash,post-do-nothing-control-missing-report
mutant=latest-cited-picks-earliest selftest-failures=2 rejected=1 cases=30 rc=1 failing-cases=post-date-inversion-committer-and-author,post-date-inversion-author-only-round45-shape
mutant=post-tip-from-local-ref selftest-failures=0 rejected=0 cases=30 rc=0 failing-cases=-
mutant=CTRL-do-nothing-pre selftest-failures=10 rejected=1 cases=30 rc=1 failing-cases=pre-dirty-tracked-file,pre-untracked-file,pre-ahead-of-remote,pre-remote-moved-by-other-writer,pre-placeholder-filled-by-L1-scorecard,pre-placeholder-lane-hash-log-bare,pre-placeholder-lane-hash-lesson,pre-backticked-quote-in-scorecard-strict,pre-round-lesson-missing,pre-do-nothing-control-no-lane
mutant=CTRL-do-nothing-post selftest-failures=15 rejected=1 cases=30 rc=1 failing-cases=post-report-with-no-cited-hash,post-unresolvable-hash,post-non-ancestor-hash,post-table-commit-column-non-ancestor,post-date-inversion-committer-and-author,post-date-inversion-author-only-round45-shape,post-two-shonen-headings,post-zero-shonen-headings,post-final-hash-not-tip,post-no-final-sentence-fails-closed,post-report-untracked-in-fleet,post-tip-moved-after-report-live-tip,post-do-nothing-control-missing-report,cli-positive,cli-two-shonen
```

Summary: 23 mutants, 20 rejected (`rejected=1`), 3 survivors (`rejected=0`): `accept-abbreviated-hashes` (HEX40 `{40}`→`{7,40}`), `date-strict-boundary` (`worst_ct <= lim` → `<`), `post-tip-from-local-ref` (post `final-is-tip` reads the local `refs/heads/master` instead of `ls-remote`). Both do-nothing controls are killed (10 and 15 failures); the unmodified gate scores 0, so the selftest discriminates against a no-op gate. Every mutant that the selftest kills is killed by an expected case, not a crash (no `CRASH` lines).

## Finding 2: the `accept-abbreviated-hashes` survivor is a real gate gap, not only a test gap

Probe `probe.py` loaded the frozen export and each survivor mutant as a module, built a fresh fixture (`make_ctx`) and ran `post_report` on three reports. Verbatim output for scenario A (report = full tip `final lane hash` plus the sentence `Lane commit \`bbbbbbb\` landed earlier.`, where `bbbbbbb` is a fabricated abbreviated hash):

```
probe mod=A-fabricated-short-hash case=g_base fail=[-] detail=cited-hashes:n=1,final=1 | resolves:unresolved=0 | ancestor:non-ancestor=0 | final-is-tip:final-not-tip=0,tip=6474bdd947a2(ls-remote) | date-order:latest-cited=6474bdd947a2@2023-11-14T22:15:00Z,report-commit-committer=2023-11-14T22:16:50Z | date-order-author:latest-cited=6474bdd947a2@2023-11-14T22:15:00Z,report-commit-author=2023-11-14T22:16:40Z
probe mod=A-fabricated-short-hash case=g_accept_abbreviated_hashes fail=[resolves,ancestor,date-order,date-order-author] detail=cited-hashes:n=2,final=1 | resolves:unresolved=bbbbbbb | ancestor:non-ancestor=bbbbbbb | final-is-tip:final-not-tip=0,tip=6474bdd947a2(ls-remote) | date-order:latest-cited=6474bdd947a2@2023-11-14T22:15:00Z,report-commit-committer=2023-11-14T22:16:50Z,unreadable=bbbbbbb | date-order-author:latest-cited=6474bdd947a2@2023-11-14T22:15:00Z,report-commit-author=2023-11-14T22:16:40Z,unreadable=bbbbbbb
```

So the frozen gate reports `fail=[-]` (exit 0) on a report that cites a commit which does not exist. Cause: `HEX40 = re.compile(r"(?<![0-9a-fA-F])[0-9a-f]{40}(?![0-9a-fA-F])")` (r46-landing-gate.py:59) only recognises 40-hex tokens, so an abbreviated citation is never collected by `cited_hashes`, and `resolves`/`ancestor`/`date-order` never see it. The docstring (lines 22-35) only promises checks over "40-hex hash" citations, so this is a scope gap in what the gate claims to verify, not a regex typo. It matters because the round-45 defect class (a report naming a lane commit that did not yet exist) is exactly what a short-hash citation would evade while a full final hash keeps the report looking valid.

Suggested edit (not applied; lane is read-only for this seat): detect 7-39 hex tokens inside trigger sentences as well, and fail closed on them (or resolve them with `cat-file` and check ancestry). Note the false-positive risk: all-hex English words of 7+ letters (e.g. `defaced`, `effaced`) would match, so the detector should require a digit or a backtick span. Add a selftest case with an abbreviated fabricated hash beside a valid final, expecting `resolves,ancestor,date-order,date-order-author` (the mutant's observed set) or a dedicated check id.

## Finding 3: `date-strict-boundary` survivor is a missing equality test

Scenario B: report committed with committer = author = the cited final commit's time (T0+100). Verbatim output:

```
probe mod=B-equal-timestamp case=g_base fail=[-] detail=cited-hashes:n=1,final=1 | ... | date-order:latest-cited=6474bdd947a2@2023-11-14T22:15:00Z,report-commit-committer=2023-11-14T22:15:00Z | date-order-author:latest-cited=6474bdd947a2@2023-11-14T22:15:00Z,report-commit-author=2023-11-14T22:15:00Z
probe mod=B-equal-timestamp case=g_date_strict_boundary fail=[date-order,date-order-author] detail=cited-hashes:n=1,final=1 | ... | date-order:latest-cited=6474bdd947a2@2023-11-14T22:15:00Z,report-commit-committer=2023-11-14T22:15:00Z | date-order-author:latest-cited=6474bdd947a2@2023-11-14T22:15:00Z,report-commit-author=2023-11-14T22:15:00Z
```

The frozen gate passes this, which matches its contract (`committer time <= committer time`). The mutant fails it. No selftest case has equal timestamps, so the boundary is unpinned. Suggested selftest case `post-date-equal-timestamp-passes`: `commit_report(ctx, report_text(ctx["c2"]), author=T0+100, committer=T0+100)`, expect no failing checks.

## Finding 4: `post-tip-from-local-ref` survivor is a missing unpushed-final case

Scenario C: final lane commit `f6c3c8b58bec` exists only locally (never pushed), report written later (author T0+400, committer T0+410). Verbatim output:

```
probe mod=C-unpushed-final case=g_base fail=[final-is-tip] detail=... | final-is-tip:final-not-tip=f6c3c8b58bec,tip=6474bdd947a2(ls-remote) | ...
probe mod=C-unpushed-final case=g_post_tip_from_local_ref fail=[-] detail=... | final-is-tip:final-not-tip=0,tip=f6c3c8b58bec(local) | ...
```

The frozen gate correctly fails `final-is-tip` against the origin tip. The mutant accepts the local-only final. Every post-report selftest case uses a pushed tip (or a `--tip` override), and the only unpushed-commit case (`pre-ahead-of-remote`) is a pre-report case, so the origin-tip read in `post_report` is unpinned. Suggested selftest case `post-unpushed-final-fails`: `lane_commit(ctx, T0+300, "unpushed final", push=False)`, report at T0+400/T0+410, expect `final-is-tip`.

## Limitations

- Mutants are single `str.replace` edits on the exact text, one per run; combinations and equivalent-mutant analysis were not attempted. "Survived" means the selftest passed, not that the behaviour was proven correct; findings 3 and 4 were checked against the frozen gate behaviour by the probe, not against a live target.
- The selftest and probes exercise only `pre_report`/`post_report` fixtures under scratch; the real `jj-lane.sh state` output was not inspected beyond what the selftest case expectations require.
- Probe results come from one fixture set (timestamps T0+*); no timezone or clock-skew variation was tried.
- Scratch under `/fast/scratch/hyaku/kasegi-r46/R46W2MutLanding` (export, mutants, probes, fixture repos) removed on exit; no tool installs; no git mutation in the lane or fleet; no edits to shared files.
