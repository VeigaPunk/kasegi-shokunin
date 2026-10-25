# Round 15 — lesson: the ground truth can be deleted mid-flight

Round: 15 (depth axis-move, forced into a source-loss re-anchor; coverage
re-based). Evidence: `LOG.md` round-15 entry, `SCORECARD.md`,
`corpus/knowledge/source-tree-loss-2026-09-28.md`, `corpus/instruments/*`,
`/tmp/kasegi-r15/*` (15 L2 reports). What generalizes:

## 1. Verify the surface exists before you plan to cite it

The round opened with a written plan inherited from r14's SCORECARD ("lift the
EV constants into `## Triage economics`"). The first command of the round —
a domain-tree snapshot, run because r14's lesson 4 said to snapshot the
append-only log at round start — returned `cd: no such file or directory`.
Every subsequent plan was different. Practice: **the first tool call of a round
touches the primary source, not the repo.** A `wc -l` on the tree you are about
to cite costs one second and catches deletion, renames, unmounted volumes and
permission loss. Had this round gone straight to editing, it would have
"re-verified" constants against a corpus copy of a file that no longer exists
anywhere and published fresh citations to nothing.

Corollary: a method error hides in the first check. `find ... 2>/dev/null`
swallowed exactly one `Permission denied` line; `find / -xdev` never enters
`/home` at all because `/home` is its own mount. Both were caught only because
a critic L2 was told to attack the *method*, not just the conclusion. When a
negative result ("it's gone") drives the round, re-run the search without
stderr suppression and without `-xdev`.

## 2. A surviving same-named file is not the same file

`~/Projects/the-bounty-hunter/ops/` still holds `ev-report.mjs`, `rank.mjs`,
`fleet-dispatch.mjs`, `claim-check.mjs`, `shared.mjs`. Naive re-anchoring would
have silently substituted mirror line numbers for lost-tree ones. The truth is
per-file, and only measurement finds it:

| file | mirror vs lost tree | how it was decided |
|---|---|---|
| `ev-report.mjs` | anchor-compatible (all 14 recorded spans, 0 offset) + **runnable-verified** | L1 read + L2 smoke run of a byte-identical copy |
| `rank.mjs` | anchor-compatible at `DEFAULTS :55-58`; the `514` consistency gate at `:136` survives | L1 read |
| `park-disposition.mjs` | anchor-compatible; the autopsy writer is **seven** parts, not five | L1 read of `:53-74` |
| `fleet-dispatch.mjs` | **diverged** — 330 lines vs 427; 3-term score at `:97` vs 5 at `:110`; different model strings; no `GRID` | L1 grep + 2 L2 derivations |
| `shared.mjs` | **earlier** — 41 lines, no `gitMutationBlocker` | L1 read |
| `claim-check.mjs` | **earlier** — 83 lines / 19 `err(` sites vs 233 / 48 | L1 grep |

Rules that follow: cite the base in the same breath as the anchor; when both
bases are known, cite both and label each; write lost-tree anchors as
`` `[lost-tree] path:line` `` so the token cannot resolve by accident; and never
call a 0-offset match "identical" — the lost bytes are gone, so identity is
unprovable, only compatibility is observable. The mirror also turned out to be
the *origin* of its GitHub remote (`.git` crtime, reflog with no clone entry,
0 packs / 48 loose objects), and 9 of 10 ops files are byte-identical to its
own initial commit — so its state is a dated snapshot, not a rolling copy.

## 3. If a metric can be satisfied by reformatting, publish the failure instead

r14 froze the bar as "the pre-edit file mean of the same run" to avoid a
circular post-edit mean. That fixed a real bug and created a worse one: the mean
ratchets (96.5 → 102.5 → 142.5 → ~167.5 projected), and the labrat measured that
the *unchanged* thin block clears 142.5 by reformatting alone (93.3 prose →
150.0 single-line-row table). So clearing the bar is not evidence of knowledge,
and failing it is not evidence of a thin section. What this round did: froze the
constant (`BAR_R15 = 142.5`), published 131.4 / 111.5 / 117.4 / 93.0 as
**not cleared**, and made the bar conjunctive with a resolvability gate from
r16 — because the mutation tester proved density rewards a fabricated
`path:line` exactly as much as a real one. A proxy that can be beaten by
wrapping is a proxy that needs a second, orthogonal instrument beside it.

## 4. Commit the instruments, or the measurement dies with /tmp

`density.py` had survived two rounds in `/tmp/kasegi-r14/` only because nothing
swept it. All three instruments now live in `corpus/instruments/` with their
definitions, known limits and the bar rule; `resolve.py` writes its census next
to itself, so the census of record is a committed artifact anyone can
regenerate and diff. An axis score whose instrument is not in the repo is not
re-derivable by a non-author — the aggregator's standing complaint about lane
scores applies with full force to a lane whose entire ground truth just
vanished.

## 5. Report the external event; do not absorb it, do not "fix" it

The tree's removal was not this lane's act and is not this lane's to undo. The
round recorded it (detection commands, window, actor candidates with for/against,
recoverability), escalated the three operator decisions it cannot make
(reorg vs deletion, recoverability, PROVINCE re-point) to `.ufo/l0-questions.md`,
reported the cross-lane blast radius (339 references across 8 lane repos; no
sibling had noticed) without editing any sibling, and pushed nothing to the
mirror's remote (outside the `MISSION.md:49-56` allow-list). Wrote zero bytes
under `~/Projects/**`. Two adjacent traps named for the next round: the attached
`ufo_sighting` tmux hosts a live external agent session (capture panes, never
send keys), and the mirror's ops scripts are runnable but must never be run in
place — all 11 derive their write root from `import.meta.url`, so a run would
mutate a read-only product repo (and would hit ENOENT on `appendLedger`, since
the mirror has no `ledger/`).

## 6. Subagent yield hygiene, again

Fifteen L2s, one batched dispatch, all read-only, all writing to distinct
`/tmp/kasegi-r15/` files — no collision this round, and three independent
reimplementations of the resolver disagreed on absolutes while agreeing on
direction. The disagreement is the finding: a rate without its definition is
unpublishable. L1 re-derived every integrated anchor itself (`anchorcheck.py`:
196 in-range instances, 0 past-EOF) and rejected two executor claims that did
not survive that check (a misplaced `[corpus-attested]` stamp on mirror-verifiable
constants, and a `:201-205` live-tree span no source records).
