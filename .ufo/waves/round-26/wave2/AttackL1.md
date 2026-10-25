# AttackL1 — claims-freeze visibility (falsify item)

Attacks: claim that the claims-freeze commit (1b076fa7 "round-26: freeze claims.json …")
is the parent of the build state, with no post-freeze edit of claims.json (byte-equal).

Verdict: **CONFIRMED — not falsified.**

## Git log (asked command)

`git log --oneline -3` in lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`:

```
1b076fa round-26: freeze claims.json (C1 gate conformance, C2 F11 assimilation) before any measurement or dispatch
2da27ea considerthese: 2026-10-25 daily reflection
b76676e round-25 verifier spot-check (integrator, hyaku): non-author admit/reject
```

## Evidence

1. Freeze commit identity (`git cat-file -p 1b076fa`): full hash
   `1b076fa7f2fb5e7dd9d87449514eba526043421b`; parent
   `2da27ea46e5cf8c992b59a6121aa62ef5e1851a6`; author/committer
   `kasegi-shokunin <kasegi@shokunin.local>`.

2. Freeze is the lane tip: `refs/heads/master` = 1b076fa. `git log --all --oneline -6`
   lists 1b076fa as the newest commit across every ref; `git reflog -5` shows
   `HEAD@{0}: 1b076fa export from jj` as the newest entry. No commit exists after the
   freeze in any ref.

3. Build state sits directly on the freeze: `git status --porcelain` shows the wave-1
   build as uncommitted working-tree changes (M: LOG.md, PROVINCE.md, SCORECARD.md,
   SKILL.md, corpus/README.md, corpus/SOURCES.md, corpus/instruments/recheck-audit.py;
   untracked: c1-controls/, c2-controls/, wave1/, wave1-*.json, c1-*.txt/json,
   knowledge entries, lessons, source-snapshots/ …). Thus the freeze commit is the
   immediate ancestor of the build state — no intervening commits.

4. No post-freeze edit of claims.json (byte-equal):
   - sha256sum of `claims.json` at 1b076fa's tree **equals** working-tree file:
     `343e568e7113f0d63ea63f7c9b8d7c18f44e310a67717d490a35ae1adec6741f` (both).
   - `git diff HEAD -- .ufo/waves/round-26/claims.json` → empty (index and worktree
     match HEAD).
   - `git status --porcelain` lists neither `M` nor `??` for `claims.json`.
   - Commits touching `claims.json` (`git log --all --oneline -- .ufo/waves/round-26/claims.json`):
     1b076fa, 5c6506c, aa8c3b4, f2eacbd. Nothing after 1b076fa touches the file.
     `5c6506c` (same freeze message) is **not** an ancestor of 1b076fa
     (`git merge-base --is-ancestor 5c6506c 1b076fa` → non-zero / "NOT ancestor"):
     it is a stale sibling export (`HEAD@{1}` in reflog) from an earlier jj attempt,
     predating the current freeze, and is irrelevant to post-freeze edits.

## Notes / unknowns

- Minor phrasing nuance: the freeze commit is not "parent of a later commit" — it IS the
  build state's commit (HEAD/master tip); the build is an uncommitted working tree on top
  of it. In the falsify sense (no post-freeze change to claims.json, freeze precedes all
  build work), the claim holds exactly.
- No installs performed (no tooling changes needed).

Milestone covered: git log freeze visibility.
