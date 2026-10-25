# OverrideAbsent — wave2 attack item

## Finding: bounty fallback can credit outside an absent explicit override

**Severity: actionable C1 falsifier.** `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-23/claims.json:4` requires bounty-prefixed mirror fallback paths to reject parent traversal outside the selected mirror and says mirror-escape fixtures should be `GONE`.

In `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/resolve.py:101-110`, a nonempty `KASEGI_MIRROR` is selected without checking that the directory exists; `MIRROR_ABSENT` records that state. In `:204-213`, the bounty fallback joins `mirror_root` with the derived suffix and returns `MIRROR-EQUIVALENT` on existence, without applying `under_mirror`. The confinement guard is only in the explicit-canonical branch at `:214-222`.

**Falsifiable fixture (not executed):** set `HOME=/tmp/override-absent-fixture/home` and `KASEGI_MIRROR=/tmp/override-absent-fixture/home/Projects/the-bounty-hunter/no-such-dir` (the selected root is absent). Create `/tmp/override-absent-fixture/home/Projects/the-bounty-hunter/ops/stale.mjs`; ensure `/tmp/override-absent-fixture/home/Projects/ops/stale.mjs` is absent. Cite `` `~/Projects/bounties/../ops/stale.mjs:1` `` in the lane `SKILL.md`. By source-path derivation, the direct bounty path misses; the fallback suffix is `../ops/stale.mjs`, so `exists_any(join(mirror_root, suffix))` reaches the stale file under `/Projects/the-bounty-hunter/ops/` and returns `MIRROR-EQUIVALENT`, outside the selected absent root. **Expected under C1: `GONE`; predicted current result: `MIRROR-EQUIVALENT`.** This specifically tests absent-override stale-root escape, not just a missing leaf under a populated override.

## Compatibility invariant

A non-traversing bounty cite with no direct bounty-tree file and a corresponding file inside the selected mirror must remain `MIRROR-EQUIVALENT`, with the reported path inside that selected root; the existing control is `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/test_resolve.py:249-253`. Preserve the existing stale-canonical/missing-override-suffix `GONE` control at `:197-209` and canonical-alias traversal/symlink controls at `:255-279`.

## Scope and verification

Static source/test review only; no tests were run and no production files were changed. The existing stale-canonical test exercises a populated override and a canonical mirror alias, while the bounty control is non-traversing; neither covers this absent-root bounty fallback. The connected tools expose no LSP device (`xd://lsp` lookup returned “No such tool”), so this review used direct file reads rather than semantic LSP checks or grep. The predicted class is a source-derived attack hypothesis, not an observed CLI result.

Report: .ufo/waves/round-23/build/OverrideAbsent.md
