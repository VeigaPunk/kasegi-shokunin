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
| M48-6 | verdict-map violation: a NUL byte inside an evidence pointer token makes the frozen counter raise an uncaught ValueError (exit 1, empty stdout, no finding line); the SKILL.md registry row maps unreadable input to exit 2; wave-1 seat `wave1/R48Review17.md` observation 1 (case 28) | none; the frozen selftest has no NUL case | Open; not fixed (counter bytes frozen after scoring). The crash fails closed, so it is not a false green and not a kill-rule trigger. Routed to round 49: a non-frozen probe that asserts exit 2 on NUL input, with the shipped bytes as positive control. Not counted as a fix. |

## Gate

S077 admitted as own-work/tier A for this lane's normative checklist form only. Opened 2026-10-30 at `/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/PROTOCOL.md`, copied byte-for-byte to `.ufo/waves/round-48/controls/protocol-source.txt`. URL: local repo path above (own-work source, no public URL asserted). Located quote, File contract SHONEN.md row: “marks are confined to the box character plus one indented evidence line per box” (14 words by `wc -w`; attempt 1 wrote 16, corrected at attempt 2 as M48-3). Canonical seed immediately follows that table. Attempt-2 re-check: the quote greps to 1 in `controls/protocol-source.txt` and in the live PROTOCOL.md; the snapshot is byte-identical to the live file (46958 bytes, `diff` 0 lines).

Admit: restoring the canonical author-assessment form. Reject: treating checker success as promotion, semantic evidence verification, an executed bounty task, or restored lost sources. Flip: independently named non-author verifier and the corresponding real domain evidence. No new knowledge entry or frontier row is admitted. No existing source status, recheck or used-by cell changes.

Independent non-author admit/reject sampling remains outstanding; lane seats are not outside verifiers. The prior round's outside spot-check agrees on S075/S076 admits and the F30 reject; that historical agreement is not this round's verification.

## Limits

The checker validates a deliberately restricted author-side grammar and existing local file pointers, not evidence meaning or independent-verifier identity. It rejects x marks rather than pretending to verify independence. Seventeen pre-freeze fixtures and six source mutants are finite evidence, not universal correctness.

Attempt-2 limits found by wave 1 and disclosed (none kills the frozen claim; see each seat report): (a) a marker-only checklist with four unchecked boxes and no evidence lines passes the frozen counter (`wave1/R48Review09.md` section 2). The claim's mechanical limits cover this; `canonical=1` must not be read as evidence of assessment substance. (b) The after-verdict depends on the tree exporting the pointer targets (`--root` requires SKILL.md, PROVINCE.md, LOG.md and the round-47 spot-check present); `measure.py` exports exactly those five paths. (c) The frozen counter accepts `- [ ]` with an evidence line, a shape no frozen fixture covers (`wave1/R48Review31.md` finding 2).

Assimilation: none — frozen-claim resume (protocol §10, "Frozen and resumed rounds"): assimilation waits for the lane's next round. Seat `wave1/R48Review13.md` screened the staged merge package and found no checklist or procedural-fit content bearing on C1. Open L0 about 22 historical gated rechecks remains unanswered (kasegi round-46 question, carried); no re-labelling. The source snapshot is a procedural source, not new bounty-domain knowledge.

## Wave-1 integration (appended 2026-10-30)

Wave 1 settled all 64 seats (`.ufo/waves/round-48/wave1-results.json`, 64 rows; 55 seat reports landed in `.ufo/waves/round-48/wave1/`). Nine rows carry an empty final payload and no report file — R48Probe28, R48Probe34, R48Probe36, R48Probe38, R48Review12, R48Review19, R48Review20, R48Review27, R48Review30 — and the handoff carries no terminal status, id or error for them: **dead-seat status is unreported, not invented as zero deaths or as success** (same handoff limitation as round 47).

No seat defeated the frozen claim. 32 box-mutant probe seats and the review seats all read the frozen checker rejecting their mutants: label byte, removed box, removed evidence line, duplicated box, HTML-comment wrap, fenced block, indent-as-code, Unicode lookalike, directory pointer, `../` traversal, absolute path, symlink escape, trailing prose, CRLF and missing final newline are each caught with a stable finding id (`SF-BOX`, `SF-EVIDENCE`, `SF-TRAILING`, `SF-PREAMBLE`, `SF-POINTER`, `SF-NEWLINE`); the positive reads `SF-CLEAN`. The frozen checker bytes (`sha256 0ab32a2c6155a7d0055196df806898cb7e78880a072bf2504143b99377b313dd`) are identical at the freeze commit and at the wave-1 integration tip: **no post-scoring amendment**. Before/after replay: base `903d47e` reads `canonical=0 finding=SF-PREAMBLE exit=1` (356 lines, 52 boxes) and the landed tree reads `canonical=1 finding=SF-CLEAN exit=0` (12 lines, 4 boxes), reproduced independently by R48Review09, R48Review24 and R48Review31.

### Disclosed limits of the frozen counter (documentation-only; the counter is not amended)

1. **Grammar, not substance.** A pristine-seed file (four `- [ ]` boxes, no evidence lines) and a file whose evidence pointer targets a 0-byte file both read `SF-CLEAN`: the checker grades shape, mark characters and pointer existence, never the truth of an assessment (R48Review09). `canonical=1` must not be read as evidence of assessment substance.
2. **Tree composition.** The after-value depends on the graded tree carrying the pointer targets: `SHONEN.md` alone in a tree reads `SF-POINTER` (R48Review09 H1/H2). The measured tree is the lane root, or the five-file export produced by `.ufo/waves/round-48/measure.py`.
3. **Author-side only.** The checker rejects `[x]` (`SF-VERIFIER`): independence cannot be established mechanically, so a non-author verifier's mark is never attested by this instrument (R48Review23).

### Sourcing precision (R48Review26)

The S077 snapshot is the canonical checkout copy `/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/PROTOCOL.md` (544 lines, `sha256 622b29a043046f0b3b3c7a2240fe62ab516898922885685dd8d89f50b1739fd0`), copied byte-for-byte to `.ufo/waves/round-48/controls/protocol-source.txt`. The fleet-root vendored `PROTOCOL.md` (533 lines, `sha256 886e459b2aa79b8198912ad54bd57fbb025cc424d78684a02fb3d4c832d4411a`) is a different vintage: whole-file bytes differ in 12 hunks, but the claim-relevant region — the File-contract `SHONEN.md` row, the canonical seed and the Marks rule — is byte-identical in both, so the frozen claim is unaffected. The drift is recorded here, not repaired.

### Criterion precision (R48Review11)

R55's grounding cell cites "R1/R2" for the round-47 spot-check routes; the same bare tokens also name QUALITY rows R1/R2 at `corpus/QUALITY.md:35-36` (`grep -n '\bR1\b' corpus/QUALITY.md` prints 6 matches, including R55's own cell at `:407`). R55 is not rewritten in place; the disambiguation is this note, and a later superseding row may reword the grounding cell. The connector also named two further tensions for a future round: R55's phrase "permitted marks" is narrower than the protocol's mark vocabulary, and the considerthese ledger's byte-pin is a content pin R55 does not cover.

### Assimilation

**None.** The staged package `/home/vgpnk/Projects/shokuknow/merge/kasegi/` holds bounty-domain entries only; none matches this round's procedural form-repair claim, and R48Review13 records the same screen. The id-collision guard was re-run read-only at the round-48 tree (R48Review14): lane registry ids and staged ids collide over the staged range (mass id drift from the package's older registry baseline), so no staged row is appendable without wholesale renumbering; **nothing is adopted this round** and no staged row was appended.

### Score attribution (R48Review28)

`depth:verifiability` stays 4 with delta 0; no 4→5 promotion limb moved (`recheck-audit.py --root . --quiet` prints `gated=22`, unchanged since round 46), the coverage frontier stays 29 rows (`r44-frontier-count.py --root . --expect 29` prints `frontier rows=29 admitted=29`), and `depth:density` stays 9. S077 is a source-registry row, not a frontier row. The seat's counterexample — that a File-contract form repair is arguably calibration ground rather than depth — is recorded: the lane scores only depth and coverage, so the lowest-axis rule points at `depth:verifiability`, whose instrument-soundness limb this repair extends (the checklist's own evidence pointers become machine-verified as resolvable).
