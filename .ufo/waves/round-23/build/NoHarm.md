# NoHarm — r23 C1 guard-count audit (read-only)

Scope: `.ufo/waves/round-23/claims.json` C1 + guard vs `corpus/instruments/resolve.py` @ `922a4dd`, `SCORECARD.md`, `corpus/QUALITY.md`, `corpus/lessons/round-23.md`, `before-instruments.json`. Host verified 2026-10-20: `~/Projects/bounties`, `~/Projects/the-bounty-hunter`, `~/Projects/origin-work`, `~/Projects/outside.md` all ABSENT.

## Falsifier F1 — the frozen-corpus "changed verdicts" count is structurally vacuous
`classify` (resolve.py:202-234) can only emit the touched verdicts (MIRROR-EQUIVALENT, and bounty-branch RESOLVES-via-literal) when `exists_any` hits. With all domain roots absent and no `KASEGI_MIRROR`, the bounty-prefix and relative mirror-fallback branches always reach their final `GONE`; `before-instruments.json` confirms `mirror=0` on the committed export. So the C1 guard's "report all changed verdicts" = 0 for the modified branches **regardless of whether the fix is correct, absent, or broken** — zero cannot distinguish confinement added from no code change at all. The guard count is not evidence of soundness; it is evidence of an absent fixture input.

## Falsifier F2 — INTERNAL growth rides the published fraction uncredited
`rate()` (resolve.py:322-327) counts INTERNAL in the numerator over whatever `.md` tree exists at run time. Round-23's own adds (uncommitted `corpus/lessons/round-23.md`, `corpus/knowledge/multiparty-*.md`, SCORECARD/QUALITY edits; pending F06–F08 entries, mirror-containment docs) add corpus path tokens that classify INTERNAL → numerator grows with zero source restoration. A single blended post-round fraction would read as availability movement even with the claim's disclaimer.

## Falsifier F3 — residual INTERNAL escape keeps the detector unsound after C1
`exists_any(join(lane_root, base))` → INTERNAL at line 227-229 performs **no** `under_mirror`-style confinement and is explicitly waived ("explicit lane-relative paths keep prior semantics"). `../outside.md` or a repo symlink to `~/Projects/x` still credits a file outside the lane. Claim text "Make MIRROR-EQUIVALENT sound" is accurate only per-class; any wording implying the detector's containment is sound is falsified by the untouched INTERNAL branch.

## Falsifier F4 — changed-verdict counting misses token-set drift
Set-level changes (a tokenization/anchor/`strip_anchor` edit that adds or drops distinct citations) never produce a "changed verdict"; they change `distinct` itself. Verdict-diff alone cannot catch it.

## Evidence
- resolve.py:204-213 bounty branch — no `under_mirror` on `exists_any(join(mirror_root, rel))` result (vs :219-221 which does apply it); `startswith(BOUNTY_PREFIXES)` also lacks `/` boundary.
- resolve.py:226-234 relative fallback — same gap; `INTERNAL` at :229 has no confinement.
- `before-instruments.json`: `distinct=1589 resolves=11 mirror=0 internal=197 gone=1381 all=208`.
- claims.json C1 `after` + SCORECARD §Round-23 already disclose "score remains 4 / no restoration credit" — disclosure exists; what is missing is a guard that can falsify the equation.

## Smallest warranted correction
1. In the count command, report the frozen-input verdict diff **labeled vacuous when `mirror=0` pre-fix**; soundness rests on the synthetic-mirror fixture matrix alone — require the fixture run, never infer it from the frozen count.
2. Publish **two** fractions: frozen base-input set vs post-round input set, and attribute the delta to input growth; score evidence pointer names both, never the blended tail number.
3. Add `distinct`/`added-tokens`/`dropped-tokens` to the reported diff, not only per-token verdict changes.
4. Name the INTERNAL branch as residual unfixed debt in the round-23 lesson so "MIRROR-EQUIVALENT sound" cannot generalize into "detector sound".

Verdict: fixable defects in guard design, not a judge-blocking tradeoff — C1's disclaimed credit is correct; the counting surface is too weak to prove the no-harm half of the claim.
