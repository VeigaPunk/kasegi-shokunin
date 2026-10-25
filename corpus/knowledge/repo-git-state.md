# Repo git state — the stalled rebase and the tracked/untracked split

Verified live 2026-09-28 (read-only; `git status/branch/rev-list/merge-base/ls-files`,
no mutation). This is the outermost provenance layer for every other corpus entry:
commit-sourced claims end 2026-09-06, but the artifacts run to 2026-09-15.

## The stall (ACTIVE hazard, ≥17 days old at census)

| Fact | Value | Basis |
|---|---|---|
| Repo state | `interactive rebase in progress; onto 7dce2872`, HEAD detached at `58acb6d8` ("chore(fleet): periodic mission-work sync [auto]", 2026-09-06T18:31:35-03:00) | `git status`, `git branch -vv` |
| Rebase stop | 1 command done (`pick 3d28a716`), **0 remaining**, "You are currently editing a commit" → stalled at the amend step; autostash present (`a00d4c55…`), `git stash list` empty | `.git/rebase-merge/{done,git-rebase-todo,autostash}` |
| Local `main` | `3d28a716`, 171 commits, author=committer date **2026-09-06T05:42:43-03:00** (round-13 correction: the earlier "18:26" matches no stamp on this commit; `58acb6d8`'s 18:31:35-03:00 confirmed) | `git branch -vv`, `rev-list --count`, `git log -1 --format=%ci` |
| `origin/main` | tip `7dce2872` (2026-09-05, "plazir lore: Halley Comet Festival…"), 180 commits; remote `github.com/VeigaPunk/bounties.git` | `git log origin/main` |
| Dirty tree | **903 entries** = 101 `M` (82 `claims/`, 6 `ops/`, 3 `evidence/`, 3 `.omp/`, 2 `ledger/`, 2 `fleets/`, 2 `docs/`, 1 `.gitignore`) + 802 `??` (307 `claims/`, 234 `evidence/`, 227 `ledger/`, `.ufo*`, root zips, `george/`, `pendle-core-v2-public/`) | `git status --porcelain` |
| Newest commit anywhere | 2026-09-06 18:31 → **all Sep 7–15 fleet work (b1k overnight, bh* audits, ingestion cycles, bpolish) is working-tree-only** | `git reflog` |
| Stall age | `[lost-tree] .ufo/grok-bounty-assessment-20260911/assessment-manifest.json:41-42` records `repository_commit: "BLOCKED_ACTIVE_PREEXISTING_REBASE"` + `clean_tree_proof: "…_AND_AMBIENT_CHANGES"` (2026-09-11) → stall predates 09-11 | manifest read |

Consequence: `[lost-tree] ops/shared.mjs::gitMutationBlocker` fail-closes with BOTH
`ACTIVE_GIT_OPERATION` and `HEAD_NOT_ON_MAIN` → every dispatcher
`commitClaims`/`finalizePush`/`periodicSync` is refused **now**. Any statement that
"the dispatcher commits/tags/pushes accepted packages" (SKILL.md mission-control
section, round-5 corpus) describes the design, not the current state. Escalated to
L0 via `.ufo/l0-questions.md` round 12 (operator decision: resolve vs intentional
freeze). Cross-domain: the fix belongs to the bounties owner.

## Tags and branches — what IS push-backed

- All **12** `claim-*` tags are ancestors of `origin/main` (pushed): 3
  `claim-ready/*` + 9 `claim-hold/*` — third-source corroboration of rounds 9–10
  (git, after `status.json` and `final-audit.json`).
- `origin/main` ancestor `56d62572` ("finalize-all: tag only DONE+claimable+unheld
  packages") states the operative invariant: **claim-ready namespace = exactly the
  3 submitted reports**; held packages under `claim-hold/*`.
- `claim-ship` (2 commits, 2026-09-04: `claim-ready:` messages for intel pqos +
  github-bug-bounty nines-CNAME) is a **merged ancestor line** (`merge-base
  --is-ancestor` rc=0, `rev-list --left-right --count origin/main...claim-ship` =
  `178 0`), not a divergent branch — and both packages are `claim-hold/*` today.
  **A historical `claim-ready:` commit message is never current authority** —
  supersession-in-place on the same history; revalidate bytes (SKILL anti-pattern
  #5). An L2's initial "disjoint branch" reading was caught by peer cross-check —
  single-witness git claims need `--is-ancestor`, not `log --oneline` eyeballing.
- `origin/main` tip is a `plazir lore:` commit: the bounties remote shares history
  with the operator's unrelated plazir project → `origin/main` is not a clean
  "bounty state" ref; the bounty state is the working tree.

## Tracking divergence — what git actually holds

| Surface | On disk | Git-tracked |
|---|---|---|
| `claims/` | 3,361 files / 274 program dirs / 295 packages | **198 files / 19 program dirs + tracked `claims/README.md`** (round-13 correction: "20 program dirs" counted the README's dir; incl. all 3 submitted + anthropic/wordpress/intel/8x8/3cx queue rows + honest-zero stubs); the cantina-pendle exemplar is `??` untracked |
| `.ufo/` | 1.5 G (bh* workspaces, bounty-fleet, sessions, assessments) | **0 files**, un-ignored except `bounty-fleet/session[s]/` |
| `fleets/run/` + `leases.json` | 703 status files, leases, portal-reconciliation | **0 — ignored by design** (`.gitignore:8-9`) |
| `george/` | 49 G | 0, untracked, un-ignored |
| `pendle-core-v2-public/` | 63 M | 0, untracked, un-ignored |
| root zips (`claim-ready-packages-2026-09-15.zip` 1.8 M / `ALL-…zip` 2.6 M) | dated snapshots | 0, untracked |
| `.gitignore` itself | 11 lines | modified-uncommitted (HEAD has 9) |

Hazards:
1. **`git add -A` ingestion risk:** 49 G `george/` + 507 M `.ufo/bh953b65628b4e` +
   63 M pendle + 1.5 G `.ufo/` are all untracked AND un-ignored — one careless
   add-all (by any tool resolving the rebase) commits gigabytes. The ignored
   622 M `bounty-fleet/session[s]/` is the only bulk that's safe.
2. **No git provenance for the audit trail:** 656 `claims/` files cite `.ufo/`
   paths (51 already dangling — see `corpus/knowledge/ufo-workspaces.md` §citations); neither side
   is versioned. The 44+ mission audit trail exists only on this filesystem.
3. **Commit-based claims must state their epoch:** "committed 9dc20e64/b01f9de4"
   citations (submitted-registry) are pre-09-06 and remain valid; anything citing
   `git log` for Sep 7–15 artifacts will silently find nothing.

## Provenance (round-22 correction, appended)

source: Lane read-only Git snapshot on 2026-09-28 — git status, branch, rev-list, merge-base, and ls-files; section The stall.
verified-at: 2026-09-28
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && test -d ~/Projects/bounties/.git && git -C ~/Projects/bounties rev-parse HEAD  # on-restoration — fails closed today: bounties base absent since 2026-09-28; the 2026-09-28 snapshot is not re-verifiable; re-scope is L0 kasegi round-15
