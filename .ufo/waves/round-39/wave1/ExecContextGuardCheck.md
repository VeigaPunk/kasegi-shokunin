# ExecContextGuardCheck — round 39 wave 1 receipt

Seat: ExecContextGuardCheck (leaf, executor). Axes: depth:verifiability, coverage.
Item: verify the wave context carries the required guard clauses so no seat can miss them; report a checklist; deliverable `ExecContextGuardCheck.context-check.txt`.

## Subject

- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-39/wave1-spec.json` (413733 bytes, sha256 `f1b6a508f7625f837305a55faa09cf82a5805bcafb0cd7929951ffcef2656bb3`), field `.context`.
- Delivery path actually used by seats: `.ufo/waves/round-39/wave1-dispatch.json` `.taskCall.context` and `.taskCall.tasks[*].task`.

## Commands and actual output

Disk guard before the pass:

```
$ bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status
root                             use%     free
/tmp                               3%   125.2G
/var/tmp                          35%   585.6G
/fast/scratch/hyaku               25%   609.8G
```

Structural inspection (`json.load`, no mutation):

```
top keys: ['wave', 'reportDir', 'maxLanes', 'axes', 'milestone', 'context', 'items']
context type/len: str 7033
items count: 49
item keys: ['name', 'role', 'axes', 'milestone', 'prompt']
```

Consolidated guard-clause matrix (five required clauses; `ctx` = occurrences in `.context`, `items` = spec item prompts containing the clause, `tasks` = dispatch task strings containing it):

```
spec_bytes=413733 spec_sha256=f1b6a508f7625f837305a55faa09cf82a5805bcafb0cd7929951ffcef2656bb3
context_chars=7033 context_utf8_bytes=7045 context_lines=20
context_sha256=0237c91d54a1a7561f73c58c938c45d0cb0609d78bd45581866e9e1c48a437b4
dispatch_context_identical=True dispatch_context_sha256=0237c91d54a1a7561f73c58c938c45d0cb0609d78bd45581866e9e1c48a437b4
SEAT_GUARD wording                     ctx=1 items=49/49 tasks=49/49
pacman pause                           ctx=1 items=49/49 tasks=49/49
no agent://all                         ctx=1 items=49/49 tasks=49/49
absolute-path-only writes              ctx=1 items=49/49 tasks=49/49
Report trailer relative to lane        ctx=1 items=49/49 tasks=49/49
items=49 dispatch_tasks=49 counts={"spawn": 49, "resume": 0, "total": 49}
task_prefix_ok=49/49
task_prefix_plus_spec_prompt_plus_tail=49/49
EXTRA lane repo only                   present=True count=1
EXTRA fleet root read-only             present=True count=1
EXTRA mutating git ban                 present=True count=1
EXTRA scratch removal                  present=True count=1
EXTRA PACMAN/uv channel                present=True count=1
EXTRA scratch root                     present=True count=1
```

Line anchors (`grep -n` over the extracted `.context` text):

```
10:Write scope. ... Every `Report:` trailer path is relative to /home/vgpnk/Projects/shokunin/kasegi-shokunin — write it at /home/vgpnk/Projects/shokunin/kasegi-shokunin/<that path>. ... Never run a mutating git/jj c…
16:Tooling. ... pacman transactions are PAUSED host-wide — never run pacman (no -S/-Sy/-Syu/-U/-R); use `uv tool install`, `npx`, or an official binary into ~/.local/bin instead; ... Never restart a host service.
18:Host guard (SEAT_GUARD). Your tools start at the fleet root: cd to your scratch first and use absolute paths for every read/write. ... Never write to any PATH directory (~/.local/bin, /usr/bin). Never write fleet-root tracked files (LOG.md, SCORECARD.md, PROVINCE.md, SHONEN.md, SKILL.md, corpus/*, MANIFEST.json at the fleet root).
20:Rules. ... Do not message agent://all. Do not run your own swarm. ... Godspeed posture governs your work ...
```

Delivery shape check: every dispatch `task` starts with `/skill:godspeed\n\n`, then the spec item prompt verbatim, then an item tail (`\n\nLane bounds: ...\nJudged on: ...\nMilestone: round-39\n\nReport: ...`). 49/49 match; shortest task 7638 bytes, longest 14893 bytes, so no truncation drops the context. Spec prompt and dispatch task differ only by that prefix and tail.

Full context occurrence counts for the five clauses are exactly 1 each; each is therefore present once per seat, not merely once in the file.

## Result

5/5 required clauses present in `.context`, 0 missing, 49/49 spec items and 49/49 dispatched tasks carry them. Extras also present (lane-repo-only, fleet-root read-only, mutating git/jj ban, scratch removal, uv/npx/binary channel, scratch root, PATH-directory and fleet-tracked-file write bans).

## Files changed

- `.ufo/waves/round-39/wave1/ExecContextGuardCheck.context-check.txt` — deliverable, 17 lines, 2065 bytes, sha256 `a6040f6d19819efc995ef3b6de274252c9260d87b80112ef8c1fab639e53e5fb`.
- `.ufo/waves/round-39/wave1/ExecContextGuardCheck.md` — this receipt.

No other lane or fleet file written. No git/jj mutation. No network fetch. No tool installed (nothing needed). Scratch `/fast/scratch/hyaku/kasegi-r39/ExecContextGuardCheck/` removed before yield.

## Risks / scope

- Check covers `wave1-spec.json` `.context` and its dispatch propagation only. The separate `# Host guard (orchestrator; applies to every seat)` block is injected outside this spec file and was therefore out of scope here.
- The five clauses live in the shared context block, once per delivered task; an item-specific prompt does not repeat them, but every dispatched task carries the block verbatim, so coverage is 49/49.
- No blocker.
