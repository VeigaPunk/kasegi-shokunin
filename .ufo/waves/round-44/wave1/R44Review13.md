# R44Review13 — C1 frozen-control accuracy

Scope: exact eight routed defects, their cited links/evidence, and whether any were already fixed at the frozen base. Read-only review; no tools installed. No scratch directory was created because `HYAKU_SCRATCH` was unset (`printf` returned empty); no scratch cleanup required. Required operator policy was read at `/home/vgpnk/.omp/agent/RULES.md`; no install/update performed.

## Base identity and do-nothing discrimination

`controls/do-nothing.txt:2` pins base `5ab3a60a5cb09e5880d11e8a1b96f9b29d368c7a (master)`. Exact command evidence:

```
git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin cat-file -t 5ab3a60a5cb09e5880d11e8a1b96f9b29d368c7a
=> commit
git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin show -s --format='%H %s' 5ab3a60a5cb09e5880d11e8a1b96f9b29d368c7a
=> 5ab3a60a5cb09e5880d11e8a1b96f9b29d368c7a round-43 verifier spot-check (integrator, hyaku): non-author admit/reject
git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin diff --name-status 5ab3a60a5cb09e5880d11e8a1b96f9b29d368c7a..HEAD -- corpus/lessons/round-43-verifier-spotcheck.md .ufo/waves/round-43/claims.json SCORECARD.md corpus/lessons/round-43.md
=> [empty]
```

The frozen list is indeed eight numbered defects: `corpus/lessons/round-43-verifier-spotcheck.md:101-108`. Its evidence points are exact and testable: composite claim at `SCORECARD.md` and r43 claims; missing checker coverage; lesson numeral; report omissions; registry/transcript/tmp hygiene; SHONEN final blank line; report pointer; and before-cell exit token mismatch. The committed spot-check's §6 expressly assigns all eight as round-44 corrections. The base is the spot-check's own lane tip per its lines 5-6 and controls line 2; there is no indication any were fixed already at that base. In particular the spot-check says the first item is unbacked, not resolved, and the eight are routed prospectively.

Do-nothing control is discriminating for the declared predicate: `controls/do-nothing.txt:4-7` records counting the numbered findings as 8 and asserts no r44 corrections/counter existed at the pinned base; the current `HEAD` is later than that base (`git rev-parse HEAD` returned `66314015122b9aa32dc40f2f1815df56624c26d1`). C1's claim requires eliminating those same items, not merely the existence of eight rows. No finding that do-nothing can satisfy C1.

## Accuracy finding

No actionable C1-control accuracy defect found in this scope. The canonical list/evidence and the do-nothing discriminator agree. I did not infer that final fixes landed: the checked-out current tree contains only the specified base plus untracked wave artifacts, and the targeted `diff --name-status` shows no change to the source records; this review does not assess later commits or the final C1 counter.

Limitations: no LSP device/server was available in the supplied tool inventory, so semantic reference/definition checks were unavailable; source and base checks above are direct committed text/Git evidence. The `git status --short` observation showed unrelated untracked `census-invocation-error.txt`, `wave1.ready.partial`, and reports R44Review1/R44Review2; none were modified. Do-nothing C2 and C1 final-state success are outside this assigned audit.