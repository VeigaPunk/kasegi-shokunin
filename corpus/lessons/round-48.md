# Round 48 — canonical checklist restoration

One frozen depth:verifiability claim, not a coverage claim. Base and predicate: `.ufo/waves/round-48/claims.json`; activity: LOG.md Round 48.

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| canonical-form drift | round-47-verifier-spotcheck.md R1; actual 356-line checklist retained at .ufo/waves/round-48/controls/shonen-before.txt | PROTOCOL File contract; previously not enforced | Restore the four-box seed with one evidence line per box. Frozen checker reads SF-PREAMBLE on actual prior bytes; candidate reads SF-CLEAN. Historical assessments remain in reports and the byte archive. |
| prose-sensitive count | round-47-verifier-spotcheck.md R2; bare supersedes S074 expression counts registry prose too | R41 whole-token rule was insufficient to distinguish rows | R55 requires row-shape anchoring and match enumeration; the real phrase-versus-row discrimination is retained under round-48 controls. Frozen round-47 bytes remain untouched. |
| M48-3 | self-assessed count error: attempt-1 Gate said the located quote is 16 words; running wc -w on the quoted text returns 14 (this lesson, Gate) | none; no lane gate checks Gate quote length | Gate word counts come from wc -w on the quoted text, and the attempt-2 Gate records the corrected count. Shown able to fail: the 16-word claim and the 14-word measurement disagree under the same command. |
| M48-4 | positive-control provenance: the frozen battery's only `canonical` fixture is the pre-freeze draft (sha b476c7aa…), not the shipped bytes (sha b1352168…); wave-1 seat `wave1/R48Review31.md` findings 1-2 | none; `measure.py` after-leg measures the shipped revision, but the frozen fixtures.json cannot be amended after scoring | Open. Not fixed this round (frozen fixtures and counter bytes are untouched). Routed to round 49 as a new non-frozen fixture file that carries the shipped bytes as positive control. Not counted as a fix. |
| M48-5 | lowest-axis label without a moved metric: C1 names depth:verifiability, but `resolve.py` censuses SKILL.md and corpus only and never reads SHONEN.md; wave-1 seat `wave1/R48Review28.md` section 1 | none; the scorecard axis rule is satisfied by label alone | Disclosed, not hidden: SCORECARD round-48 section states score held at 4 with delta 0 and names the metric that did not move. Routed to round 49: the lowest-axis claim must move a metric the axis counter reads. |

## Gate

S077 admitted as own-work/tier A for this lane's normative checklist form only. Opened 2026-10-30 at `/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/PROTOCOL.md`, copied byte-for-byte to `.ufo/waves/round-48/controls/protocol-source.txt`. URL: local repo path above (own-work source, no public URL asserted). Located quote, File contract SHONEN.md row: “marks are confined to the box character plus one indented evidence line per box” (14 words by `wc -w`; attempt 1 wrote 16, corrected at attempt 2 as M48-3). Canonical seed immediately follows that table. Attempt-2 re-check: the quote greps to 1 in `controls/protocol-source.txt` and in the live PROTOCOL.md; the snapshot is byte-identical to the live file (46958 bytes, `diff` 0 lines).

Admit: restoring the canonical author-assessment form. Reject: treating checker success as promotion, semantic evidence verification, an executed bounty task, or restored lost sources. Flip: independently named non-author verifier and the corresponding real domain evidence. No new knowledge entry or frontier row is admitted. No existing source status, recheck or used-by cell changes.

Independent non-author admit/reject sampling remains outstanding; lane seats are not outside verifiers. The prior round's outside spot-check agrees on S075/S076 admits and the F30 reject; that historical agreement is not this round's verification.

## Limits

The checker validates a deliberately restricted author-side grammar and existing local file pointers, not evidence meaning or independent-verifier identity. It rejects x marks rather than pretending to verify independence. Seventeen pre-freeze fixtures and six source mutants are finite evidence, not universal correctness.

Attempt-2 limits found by wave 1 and disclosed (none kills the frozen claim; see each seat report): (a) a marker-only checklist with four unchecked boxes and no evidence lines passes the frozen counter (`wave1/R48Review09.md` section 2). The claim's mechanical limits cover this; `canonical=1` must not be read as evidence of assessment substance. (b) The after-verdict depends on the tree exporting the pointer targets (`--root` requires SKILL.md, PROVINCE.md, LOG.md and the round-47 spot-check present); `measure.py` exports exactly those five paths. (c) The frozen counter accepts `- [ ]` with an evidence line, a shape no frozen fixture covers (`wave1/R48Review31.md` finding 2).

Assimilation: none — frozen-claim resume (protocol §10, "Frozen and resumed rounds"): assimilation waits for the lane's next round. Seat `wave1/R48Review13.md` screened the staged merge package and found no checklist or procedural-fit content bearing on C1. Open L0 about 22 historical gated rechecks remains unanswered (kasegi round-46 question, carried); no re-labelling. The source snapshot is a procedural source, not new bounty-domain knowledge.
