# FleetScope — round 23

**Severity: Moderate (conditional cross-workspace write risk; no misdirected write observed).** Axes reviewed: `depth:verifiability`, `coverage`. This is an evidence-path/integrity finding only; it does not prove or refute frozen claims C1/C2 and is not admission credit.

## Finding: emitted relative report trailer is not bound to the lane repository root

Frozen contract in `.ufo/waves/round-23/build-spec.json:3-4` says report paths are relative to `/home/vgpnk/Projects/shokunin/kasegi-shokunin` and must be written at that absolute root. The frozen assignment (`build-spec.json:376`) is read-only except for its assigned report. The actual dispatch payload (`build-dispatch.json`, `.taskCall.tasks[] | select(.name == "FleetScope")`) emits:

```text
Report: write your scoped findings to .ufo/waves/round-23/build/FleetScope.md
```

The upstream wave renderer `/home/vgpnk/Projects/ufo-fsd-alpha/scripts/ufo-swarm-wave.mjs:208-209` builds that text by interpolating `reportDir/name.md` without an absolute root. Its `validateRelativePath` / `validateReportDir` (`:380-397`) rejects traversal and absolute spellings, but does not bind the report destination to the lane's actual working directory. Registry paths are separately rooted with `resolveBeneathRoot(ROOT, ...)` (`:411-425`); the emitted report path does not use that gate.

Observed shell `pwd` was `/home/vgpnk/Projects/shokunin`; Kasegi is the child repo `/home/vgpnk/Projects/shokunin/kasegi-shokunin`. **[INFERENCE]** If a lane's file-write tool resolves the literal trailer against that observed cwd instead of the explicit contract root, it targets `/home/vgpnk/Projects/shokunin/.ufo/waves/round-23/build/FleetScope.md`, one directory above the intended lane report. That can misplace a report in the fleet/sibling workspace or fail to deliver it. This is falsifiable by confirming each lane's effective cwd and the resolved path at its write boundary.

No wrong-tree report was observed at inspection: the parent `/home/vgpnk/Projects/shokunin/.ufo/waves/round-23` was absent, while the target repo's `build/` contained only `swarm-registry.json`. The dispatch/run evidence does not record the eventual path actually passed to each lane's `write` tool.

**Smallest remediation / invariant:** preserve the required relative trailer, but require every writer to resolve it against the explicit absolute Kasegi repo root and pass the resulting absolute path; before writing, assert the canonical parent remains beneath that root. Do not infer the write root from inherited cwd. For production changes, use a private clone and let L1 integrate.

## Private-clone and index observations

The target repo was at frozen base `922a4dde90b60b465e2b8b241d1fe363f1f27e98` when inspected. Two relevant private clones were observed under `/tmp`:

- `/tmp/kasegi-r23-FixMirror-5`: same HEAD; `git status` showed only `M corpus/instruments/resolve.py` and `M corpus/instruments/test_resolve.py`.
- `/tmp/kasegi-r23-RecheckSources-5`: same HEAD; `git status` showed only `?? corpus/instruments/source-recheck.py`.

The target repo status at that observation did **not** show those three paths as modified/untracked; `source-recheck.py` was absent from the target. `stat` showed clone `resolve.py` and packed-object files on device 66305 with distinct inodes from the target repo on device 57; the clone and target `.git/index` files likewise had distinct inodes. This supports isolated worktrees/object packs/indexes for these two clones. It is not proof for all 64 lanes or that every clone command used the required flag.

The target worktree was not clean overall: `SCORECARD.md` and `corpus/QUALITY.md` were modified; `.ufo/waves/`, two round-23 knowledge entries, and `corpus/source-snapshots/` were untracked. I cannot attribute those files to L1 versus other actors from the inspected evidence. The displayed status had no staged paths, but is only a point-in-time view; no pre/post index digest was available. No explicit `git add`, commit, reset, push, or JJ operation was run. **Caveat:** I invoked `git status` on the target and two private clones for this review; ordinary Git may refresh cached stat data in an index, and I did not capture a before/after index digest, so I cannot certify byte-for-byte index immutability from this review.

## Scope limits

No external targets, tests, builds, or formatters were run. I inspected the frozen claims/assignment, round-23 dispatch and registry, wave renderer/tests, target repo status, and the two named clones only. I did not inspect every lane's live cwd, every clone, the fleet repo's full status, or JJ state; absence of those observations is not evidence that no other actor wrote there.
