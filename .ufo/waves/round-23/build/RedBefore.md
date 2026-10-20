# RedBefore — fail-before/same-input audit of r23 frozen claims (read-only, critic)

Scope: `claims.json`, `SCORECARD.md`, `corpus/QUALITY.md`, `corpus/lessons/round-23.md`,
`corpus/instruments/{resolve,test_resolve,source-recheck}.py`, `corpus/SOURCES.md`,
the three new knowledge entries, `.ufo/waves/round-23/{build-spec,before-instruments}.json`.
Read-only: no resolver, test, or recheck command was executed; all verdicts below are
static derivations from `classify` at `922a4dde` plus observed working-tree state.

## F1 — depth:verifiability (C1): the frozen "before" covers one of three defective branches; relative-fallback fix can land vacuously

Evidence (all at `922a4dde`):
- `resolve.py:204` — `base.startswith(BOUNTY_PREFIXES)` has no `/` boundary.
  `~/Projects/bounties-x/...` enters the bounty domain; `rel` becomes `-x/...`; if the
  literal is absent, `join(mirror,"-x/...")` credits MIRROR-EQUIVALENT for a sibling
  root (`:206`,`:210-212`). `mirror_suffix` (`:184-190`) already has the boundary;
  the bounty domain does not — asymmetric.
- `resolve.py:210-212` (bounty fallback) and `:230-233` (relative fallback) call
  `exists_any` without `under_mirror`; realpath confinement exists only on the
  canonical branch (`:220`). `exists_any` (`:163-177`) can return literal, brace, or
  glob hits — every one can escape via `../` segments or a symlinked component.
- `claims.json before_observed` records a pre-fix verdict for exactly ONE input:
  the bounty-parent case. The recorded `../outside.md → INTERNAL` resolves via
  `lane/../outside.md` at `:227-229` — the lane branch, not the mirror fallback.
  For the relative-fallback escape (`join(mirror,"../outside.md")` reaching
  `dirname(mirror)`) no before verdict exists anywhere frozen.
- `test_resolve.py:15-25` docstring: every existing confinement case
  (`test_dotdot_escape_…`, `test_symlink_inside_mirror_…`) targets the canonical
  branch and is recorded as "PASS on both baseline and fixed bytes". The new defect
  class currently has zero fail-before coverage.

Falsifier: for any declared escape fixture, if the baseline-resolver replay is absent
or prints the same class as the fixed resolver, C1's "fail before" is unproven —
the claim fails on that case. In particular: a relative-escape fixture whose builder
places the escape target adjacent to BOTH `lane` and `mirror` (e.g. mirror and lane
siblings under one fixture parent) flips to INTERNAL on both revisions — a vacuous
pass indistinguishable from a working fix.

Smallest warranted correction (all four, none optional):
1. C1 evidence = per-case (baseline TSV class, fixed TSV class) pairs over ONE
   committed fixture matrix; CountMirror's `--resolver` comparison must be exercised
   against `922a4dde` `resolve.py` bytes, not only asserted to exist.
2. The matrix needs a dedicated relative-fallback case: lane-side parent absent AND
   escape target present at `dirname(mirror)`. Pin per-case absence/presence
   assertions so vacuity is detectable.
3. Expected classes must distinguish literal-present prefix-sibling (RESOLVES —
   truthful literal) from literal-absent sibling (GONE, never MIRROR-EQUIVALENT).
   "All declared fixtures → GONE" over-corrects a literal-present case.
4. `under_mirror(p, mirror_root)` must wrap the RESOLVED path `p` for all three
   `exists_any` methods at `:211` and `:232`; a lexical prefix check on the joined
   string misses symlink escapes through existing components. Do not restrict the
   literal `exists_any(base)` RESOLVES at `:207` — literal existence is out of claim
   scope and restricting it flips truthful RESOLVES → GONE.

## F2 — coverage (C2): the recheck apparatus the three new `recheck:` lines invoke does not exist on committed bytes

Evidence:
- All three new entries carry `recheck: python3 corpus/instruments/source-recheck.py
  --manifest corpus/source-snapshots/round-23/manifest.json --source S0xx`.
- `find` over the lane tree finds NO `manifest.json`;
  `corpus/source-snapshots/round-23/` contains only `S018.txt`, `S029.txt`, `S030.txt`.
- `git status`: `source-recheck.py`, `corpus/source-snapshots/`, and all three
  knowledge entries are untracked (`??`). With the manifest absent the instrument's
  own code path emits `manifest UNAVAILABLE reason=missing` → exit 2.
Falsifier: if `corpus/README.md` F06–F08 flip to `admitted` at a revision where the
recheck exits 2 (missing manifest/instrument/snapshot), Q1's runnable-command
requirement and Q7's failing-control requirement both fail — C2 cannot claim 3/3.
Smallest correction: instrument + manifest + snapshots land at the same revision as
the row flips; C2 evidence = three exit-0 outputs at the measured commit plus at
least one demonstrated corrupt/missing-source control exiting nonzero (Q7).

## F3 — evidence-form substitution risk (R7-adjacent, C1)

`claims.json` freezes the detector as "resolve.py classify plus copied real CLI TSV".
Evidence quoting `test_resolve.py` unittest pass-names or `mirror-containment-check.py`
selftest totals in place of per-citation TSV `class` columns from both resolver
revisions is the forbidden separate-selftest shape. Correction: report format =
fixture citation → baseline TSV class → fixed TSV class, plus the frozen SKILL/corpus
no-harm diff disclosing every changed verdict (claim `guard`). Also: if new escape
tests join `test_resolve.py`, its docstring's "fail on baseline" roster
(`:15-25`) must name them — else the recorded baseline map is itself stale (R3).

## Scope limits

- Working tree observed mid-flight (uncommitted wave output); F2 is conditional on
  the admitted revision and remains checkable post-landing.
- No commands executed; `MIRROR-EQUIVALENT`-before verdicts are static derivations,
  which is itself the gap: the frozen `before_observed` is prose for one input only.
- Out of scope: F06–F08 quote-vs-source verification (other seats); score level
  (correctly held at 4/7 per claims).
