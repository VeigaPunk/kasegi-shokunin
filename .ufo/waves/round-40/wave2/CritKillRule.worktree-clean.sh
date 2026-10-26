#!/usr/bin/env bash
# CritKillRule.worktree-clean.sh — round-40 wave-2 attack fixture.
# Attacker: CritKillRule (critic seat, C1 kill rule).
# Target: the frozen kill-rule clause "lane working tree not clean at filing",
#   enforced (per scripts/hyaku/closure-prompt.md) with
#   `git -C <lane> status --porcelain`.
# Purpose: show a working tree that APPEARS clean while a file changed — i.e.
#   a real defect (uncommitted change) present while the kill rule does not
#   fire. Two mechanisms are demonstrated in a fresh fixture repo:
#     (a) `git update-index --skip-worktree` (same for --assume-unchanged) on
#         a tracked file: content changes vanish from `git status --porcelain`
#   A control proves the same change IS visible without the flag.
# usage: bash CritKillRule.worktree-clean.sh
set -u
D=$(mktemp -d "${TMPDIR:-/tmp}/wtclean.XXXXXX") || exit 2
trap 'rm -rf -- "$D"' EXIT
cd "$D" || exit 2
git init -q .
[ "$(git rev-parse --show-toplevel)" = "$D" ] || { echo "fixture guard failed"; exit 2; }
git config user.email t@t; git config user.name t
printf 'v1\n' > tracked.txt
mkdir -p sub
printf 'sub/\n' > .gitignore
git add -A && git commit -qm init

echo "== (a) skip-worktree hides a tracked-file change =="
git update-index --skip-worktree tracked.txt
printf 'v1-exfiltrated\n' > tracked.txt
printf 'git status --porcelain: [%s]\n' "$(git status --porcelain)"
printf 'git diff HEAD stat:     [%s]\n' "$(git diff --stat HEAD)"
echo "== (b) .gitignore hides an untracked file =="
printf 'junk\n' > sub/ignored-new
printf 'git status --porcelain: [%s]\n' "$(git status --porcelain)"
echo "== control: same change without the flag is visible =="
git update-index --no-skip-worktree tracked.txt
git checkout -- tracked.txt
printf 'v2-dirty\n' > tracked.txt
printf 'git status --porcelain: [%s]\n' "$(git status --porcelain)"
