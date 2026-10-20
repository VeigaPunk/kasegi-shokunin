# LaneRelative — round23, C1 (MIRROR-EQUIVALENT soundness), lane-relative `../` citations

Seat: KasegiR23.LaneRelative-5 (reviewer, read-only). Base: 922a4dde90b60b465e2b8b241d1fe363f1f27e98.
Scope: `corpus/instruments/resolve.py`, `corpus/instruments/test_resolve.py`, frozen C1 in
`.ufo/waves/round-23/claims.json:4`. No repo edits, no test runs. Behavior checks were neutral
`os.path` semantics in a removed `/tmp/lanecheck-*` scratch dir; no repo code executed.

## 1. Exact code lines (observed at base)

`corpus/instruments/resolve.py`:

- :90 `BOUNTY_PREFIXES = ("~/Projects/bounties", "/home/vgpnk/Projects/bounties")`
- :163-177 `exists_any` — literal `os.path.exists`, then brace, then glob; **no confinement of any kind**.
- :180-191 `mirror_suffix` — exact canonical alias only: `base == root` or `base.startswith(root + "/")`; prefix siblings correctly rejected here.
- :194-199 `under_mirror` — realpath containment (`os.path.commonpath((r, p)) == r`); catches both `..` walk-outs and symlink escapes. Correct, but only **one** call site.
- :202-234 `classify`:
  - :204-213 bounty branch: `startswith(BOUNTY_PREFIXES)`; `rel = base.split("/Projects/bounties", 1)[1].lstrip("/")`; canonical hit `exists_any(base)`; then fallback `exists_any(os.path.join(mirror_root, rel))` → `MIRROR-EQUIVALENT` at :211-212 **without `under_mirror`**.
  - :214-222 canonical-alias branch: the only confined one — `if m and under_mirror(p, mirror_root)` at :220.
  - :223-225 other explicit roots: plain exists/`GONE`.
  - :226-229 relative → lane first: `exists_any(os.path.join(lane_root, base))` → `INTERNAL` at :228-229. `base` here may contain `../` and the joined path may resolve **outside the lane repo** — intentional prior semantics.
  - :230-234 relative mirror fallback: guard is `if base not in ("", ".", "..")` — exact-string match only, so every `../x` base passes; `exists_any(os.path.join(mirror_root, base))` → `MIRROR-EQUIVALENT` at :232-233 **without `under_mirror`**.
- :444-446 r5 ambiguity list re-runs the same unconfined `exists_any(os.path.join(mirror, base))` (cosmetic: affects only the .md ambiguity list, never a class).

`corpus/instruments/test_resolve.py` (observed at base):

- :71-74 fixture: `mirror = <fix>/relocated/tbh`, `KASEGI_MIRROR` override, fake `HOME`.
- :213-235 `test_relative_precedence_internal_then_mirror_then_gone` — lane-first INTERNAL, mirror-only MIRROR-EQUIVALENT, absent GONE (no `../` bases here).
- :240-243 `test_bounty_control_relative_under_mirror` — confined bounty positive control only (`~/Projects/bounties/fleet/queue-stats.json:1` → mirror `fleet/queue-stats.json`).
- :245-264 `test_dotdot_escape_from_new_mapping_is_confined` — tokens are canonical aliases (`~/Projects/the-bounty-hunter/../outside-vault/secret.mjs:1` and the expanded-home CAND2 form); they take the :214-222 branch and already classify GONE on baseline. **Does not exercise the bounty or relative fallback branches.**
- :266-272 `test_symlink_inside_mirror_escaping_root_is_confined` — same canonical-alias branch only.
- Net coverage gap: no test drives a `..`-escape through the bounty fallback (:210-212) or the relative fallback (:231-233), and no test pins a lane-relative `../` INTERNAL control.

## 2. Counterexample (falsifiable; wave2 attack item)

Citation token `` `../outside-vault/secret.mjs:1` `` placed in the fixture lane `SKILL.md`;
fixture per `test_resolve.py:71-74` (`KASEGI_MIRROR=<fix>/relocated/tbh`, fake `HOME`);
a real file at `<fix>/outside-vault/secret.mjs` (the exact construction the canonical test
uses at `test_resolve.py:255-264`, i.e. one level **above** the mirror root); no file at
`<fix>/lane/../outside-vault/secret.mjs` so the lane candidate misses.

Static trace at base: `strip_anchor` drops `:1` (:137-145); :204 no; :214 `mirror_suffix` → None;
:223 no; :227 `join(lane, base)` absent → no INTERNAL; :230 `"../outside-vault/secret.mjs" ∉ ("", ".", "..")`
→ passes; :231 `join(mirror, base)` = `<fix>/relocated/tbh/../outside-vault/secret.mjs` exists
literally → :232-233 returns **MIRROR-EQUIVALENT** with resolved path whose realpath is
`<fix>/outside-vault/secret.mjs`, outside `realpath(mirror)`.

Neutral scratch verification (removed `/tmp/lanecheck-*`): `os.path.exists(join(mirror,"../outside-vault/secret.mjs"))`
→ `True`; its realpath inside the mirror → `False`; `join(lane,"../fleet/INTEGRATION.md")` exists → `True`
(lane walk-out resolves); bounty `rel` extraction of `~/Projects/bounties/../outside.md` → `'../outside.md'`.

- **Observed (current) class: MIRROR-EQUIVALENT** crediting a file outside the selected mirror.
- **Expected class after C1: GONE** (domain `rel`), because `under_mirror(p, mirror_root)` (:194-199)
  is False for that hit — the same predicate the canonical branch already applies at :220.
- Same defect shape through the bounty branch: `~/Projects/bounties/../outside-vault/secret.mjs:1`
  → `rel = ../outside-vault/secret.mjs` (:206) → unchecked fallback at :210-212 (corroborated
  independently by RangeLimits.md and FixMirror.md; not executed by this seat). Symlink variant:
  a mirror-internal symlink pointing outside is credited by both fallbacks identically, since
  `exists_any` returns the link path and no realpath check runs.

## 3. Compatibility invariant (do not over-constrain)

Lane-relative `..` citations are intentional prior semantics and must survive C1 byte-for-byte:

- Frozen: claims.json C1 `before_observed` — "relative ../outside.md is INTERNAL (not targeted:
  explicit lane-relative paths keep prior semantics)".
- Live rows: `../MISSION.md:49-56` is INTERNAL in the generated census
  (`corpus/instruments/citation-survival.md:109`, resolved
  `/home/vgpnk/Projects/shokunin/kasegi-shokunin/../MISSION.md` — outside the lane repo, by design);
  `../../../.ufo/l0-questions.md` (`corpus/README.md:54`), `../.ufo/l0-questions.md`
  (`LOG.md:549`, `PROVINCE.md:14`), `../MISSION.md` (`SCORECARD.md:3`), `../.ufo/waves/...`
  (`corpus/lessons/round-20-recensus.md:4`), `../CORPUS.md` (`LOG.md:20`) all resolve via :227-229.
- Therefore a conforming fix: (a) adds `under_mirror` **only** to the mirror-fallback hits at
  :210-212 and :231-233; (b) leaves the lane candidate at :227-229 unconfined and un-gated;
  (c) does **not** widen the :230 exclusion to all `..`-containing bases (that would flip the
  live `../MISSION.md` / `../../../.ufo/l0-questions.md` INTERNAL rows to GONE or to
  MIRROR-EQUIVALENT, silently rewriting historical census rows); (d) keeps
  `test_relative_precedence_internal_then_mirror_then_gone` (:213-235) and the confined bounty
  control (:240-243) passing; (e) wave2 should add an explicit lane-relative `../` INTERNAL
  control plus the two fallback-escape negatives to the copied-CLI matrix.
- After the fix, the module docstring REL policy (:44-49, "else exists under mirror?
  MIRROR-EQUIVALENT") needs the confinement qualifier or docs will contradict behavior.

## 4. Secondary observation (bounty sibling-prefix; C1 claims prefix-confusion rejection)

:204 `base.startswith(BOUNTY_PREFIXES)` has no path-boundary check: `~/Projects/bounties-x/f.md`
starts with `"~/Projects/bounties"` → routed into the bounty branch, `rel` becomes `-x/f.md`
(:206 split on the first `/Projects/bounties`), and a stray `-x/` directory under the mirror
would credit MIRROR-EQUIVALENT for a token whose canonical target is a different root. Expected
post-C1: sibling roots keep plain other-root semantics (exists→RESOLVES else GONE), mirroring
`test_prefix_sibling_roots_keep_other_root_behavior` (:229-238) which covers only the canonical
mirror sibling, not the bounty-prefix sibling. Cross-seat note for DirectBounty/BountyParent.

## 5. Scope limits

Static analysis of the two files at the frozen base only; no clone edits, no CLI or detector
runs, no `/tmp` fixture with repo code executed (neutral `os.path` checks only). Classes named
"observed (current)" are derived from the code path, corroborated by the baseline-fail test
docstring (`test_resolve.py:22-31`) and sibling reports; "expected" classes are normative C1
requirements, not measured outcomes. No admission, score, or acceptance credit claimed.
