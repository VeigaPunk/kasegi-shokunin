# AxisFit — C1 detector-soundness critique (round 23, read-only)

Seat: KasegiR23.AxisFit-5. Target: `claims.json` C1 (depth:verifiability,
`corpus/instruments/resolve.py` MIRROR-EQUIVALENT confinement). Base
`922a4dde90b60b465e2b8b241d1fe363f1f27e98` read: `resolve.py:90-234`,
`test_resolve.py:175-279`, `SCORECARD.md:33-47,363-392`, `QUALITY.md` R3/R7,
frozen census `citation-survival.tsv` (1480 rows). No edits, no checks run
against the detector.

## Measurement correctness vs availability — the distinction holds, partially

C1 is instrument correctness, not availability: it changes which verdicts the
detector *reports*, not which files exist. That is legitimate
depth:verifiability work under the lane's own rules — `QUALITY.md` R7 was
minted for exactly this ("instrument-correctness claims must change and
exercise the actual detector"), and the r17-continuation row
(`SCORECARD.md:200-204`) set the precedent of crediting measurement correctness
under this axis with score held. The claim is honest about it ("Score remains
4; no source availability restoration"). **The axis fit is sound provided the
fixture matrix actually exercises the defect class — see falsifiers.**

## Reachability (verified this session, not inferred)

`test -e`: `~/Projects/bounties`, `~/Projects/the-bounty-hunter`,
`~/Projects/origin-work` are ALL ABSENT. Every bounty/mirror fallback branch in
`classify()` (`resolve.py:204-234`) is dead code on the live filesystem; the
frozen TSV shows every `~/Projects/bounties*` row GONE and zero
MIRROR-EQUIVALENT rows producible. Therefore: the defect C1 fixes cannot fire
on any real corpus token today; the before→after evidence is 100% synthetic
fixtures; the live-census changed-verdict disclosure will be ~zero. This is a
scope limit, not a defect — but it raises the bar: the fixture matrix IS the
entire evidence base, so any missing fixture class leaves soundness unproven
in exactly the restored-mirror regime the fix exists to protect.

## Falsifier 1 (strongest): RESOLVES branch of the bounty prefix keeps the traversal credit

`resolve.py:207-209`: `exists_any(base)` on `~/Projects/bounties/../../x.md`
resolves lexically and, in any regime where the `bounties` root exists
(restored, relocated, or symlinked), credits an out-of-root file as RESOLVES
under domain `bounty`. The claim text — "bounty-prefixed ... paths cannot
credit parent traversal" — is only enforced for the GONE half; the RESOLVES
half retains exactly the traversal credit the claim forbids. Invisible to any
fixture without a populated bounty root. Counterexample token:
`~/Projects/bounties/../sibling/secret.md` with `bounties/` present and
`~/Projects/sibling/secret.md` existing → RESOLVES today, still RESOLVES after
a fallback-only fix.

## Falsifier 2: `exists_any` methods bypass confinement unless the resolved path is gated

`exists_any` (`:163-177`) returns `(method, resolved_path)` where the returned
path can leave the mirror: sorted-first glob match may be a symlink escape;
`../` in rel survives `join`; placeholder `*` can match outside. Confinement
must apply to `p` (the resolved path) via `under_mirror`, not to the joined
string — a string-prefix or lexical `..`-ban implementation passes naive
escape fixtures while either still crediting glob escapes or falsely killing
confined `sub/../x` citations. Fixture required: rel/glob token whose first
sorted mirror match escapes → GONE; plus `sub/../x.md` staying in-mirror →
MIRROR-EQUIVALENT (the claim's own "preserve valid confined mirror" positive
control; a lexical ban regresses it to GONE).

## Falsifier 3 (scope limit): INTERNAL `../` escapes are the same traversal class, reachable TODAY

`resolve.py:227-229`: `exists_any(join(lane_root,"../sibling-lane/x.md"))` →
INTERNAL, crediting confinement-classed evidence for a file outside the lane —
live right now (`~/Projects` has 20+ sibling lanes), needing no mirror. The
claim excludes it ("explicit lane-relative paths keep prior semantics"), so
the reachable instance of the identical defect class survives while the
unreachable mirror instances are fixed. Truthfulness caveat: the escaped file
does open, so the axis fraction stays honest; the defect is the
confinement-class semantics asymmetry, weaker than F1 but real.

## Falsifier 4 (wording): "reject sibling-root prefix confusion" overclaims

After a correct boundary fix (`base == p or base.startswith(p + "/")`),
`~/Projects/bounties-evil/x.md` falls to the generic absolute branch →
RESOLVES when the file exists — credited, not rejected. Only mirror credit is
rejected. Fixture should assert RESOLVES/domain-"other" for an existing
sibling-root file; claim wording should be "no mirror credit for prefix
siblings." Domain flips bounty→other belong in the changed-verdicts
disclosure.

## Smallest safe correction

1. Gate the bounty RESOLVES result with the same `under_mirror`-style realpath
   check against the bounty root (or record traversal RESOLVES as a named
   non-goal; but then the claim sentence must be narrowed).
2. Reuse `under_mirror` verbatim on the `exists_any` resolved path in both
   fallback branches; add the four fixture classes above (in-root traversal
   with populated root; glob/symlink escape; confined `sub/../x` positive
   control; existing sibling-root file).
3. Record F3 and F4 as named residual debt in `corpus/lessons/round-23.md` so
   the soundness claim reads "mirror-credit confinement," not "traversal
   soundness."

Impacted axis: depth:verifiability only; coverage (C2) and density untouched
except the disclosed census regeneration.
