# R47W2D5Payload — final integrated D5 review

Axes: depth:verifiability; coverage. Static review only; recommendation, not admission.

Revision: `65e19bdb142c90a08103eb4b2af60c71218a920e`; base: `fc8e0af27fbfa13220cd245700e9cb7e5e94dfc8`; freeze: `308a2cb2dc7bdce233461cc1ac49dd88e51c6193`.

## Findings by severity

No actionable D5 defect found. All three round-46 payloads are byte-identical, occur exactly once as complete lines, and now occupy their intended rendered sections. No drafting scaffold or code fence remains in `corpus/SOURCES.md`.

**Claim boundary — not a target pass:** C1 remains not fully met and C2 remains unmet. The committed `corpus/lessons/round-47.md:59-60,65-69` explicitly preserves the harmful-transition conflict and F02-overlap decision. Correct D5 landing does not establish either frozen target. No target was rerolled or runtime gate invoked in this review.

## Independent committed-byte evidence

Fetched both `corpus/SOURCES.md` Git objects with read-only `git show REV:corpus/SOURCES.md`; compared raw bytes using Python `splitlines(keepends=True)`, equality, occurrence counting and SHA-256. No working-tree or W1 draft substituted for the assigned revision. Lengths include the terminating LF.

| Payload | Base line → integrated line | Bytes | SHA-256 |
|---|---|---:|---|
| F29 search sweep | 122 → 115 | 2504 | `9d45acb40b2061aad660306919ca8d0f073231d81dc484d3ebf9052737e6ffdf` |
| S074 row-added history | 183 → 172 | 1095 | `374d7d75291d5062b69f2bc6e1afe5cfb0faee03a66deec66b6128424d2b9ada` |
| Capture-directory note | 184 → 173 | 978 | `94c88984da5448fd3d95621fefd58cf32b181d8245984694d0e9245ceaf6d198` |

All three comparisons equal, each with exactly one complete-line occurrence. These independently reproduce the original payload digests documented in `.ufo/waves/round-47/w1/R47RevD5.md:32-40`, now against the final integrated object rather than the proposal.

Placement:
- Search-log heading `corpus/SOURCES.md:93`; preceding F28 bullet `:113`; blank `:114`; F29 `:115`; blank `:116`; new round-47 study `:117`; Leads heading `:119`. Thus F29 is an ordinary Search-log bullet immediately after F28, not inside Leads or a fence.
- Registry-changes heading `:126`; historical S074 and capture-note bullets `:172-173`, adjacent and in that section, surrounded by blank lines `:171,174`. New round-47 registry history follows `:175-177`. Being no longer the final EOF lines is expected additional integrated history, not misplaced payload.
- Compared the complete base→revision textual diff, including every deleted scaffold line. All nine prose lines (base `:113,115-119,177,179-180`) are absent; all four fence lines (base `:121,123,182,185`) are absent. Whole-file searches find zero backtick fences, zero tilde-fence openers, zero `to append`, and zero occurrences of each of the eight title/instruction/continuation phrases recorded in the receipt. This covers wrapped instruction continuations, not merely the two headings.

Object identities:
- Base: 124448 bytes, 185 lines; SHA-256 `e3bdefcfaad97e093a2950af37e62430635f130d9ea2d43fb1585db988077a6c`.
- Integrated: 127946 bytes, 177 lines; SHA-256 `2d3d1d15eeffc10f6803500dbf1535cec05a0423ae6b468c269337e3e1f257b8`.

Receipt: `.ufo/waves/round-47/w2/R47W2D5Payload.receipt.json` (exact identities, payload lengths/hashes, placement and scaffold absence checks).

## Residual risk and verification gaps

- Static byte analysis executed; project runtime, counters, selftests, mutation battery, live-source requests and semantic admission checks **unrun**, as required for this reviewer. This is not a saturation claim or a count toward 32 executed runtime attacks.
- `read xd://lsp` returned `No such tool`; no LSP status/references/definition/diagnostics endpoint is mounted. Literal byte inspection is fallback evidence, not semantic-reference proof. No runtime/caller/resume changes are in this bounded document-only assignment.
- W1 proposal offsets `:170-171` are historical; final integrated offsets are `:172-173`. Historical captures and reports were not rewritten. The verbatim S074 bullet records the original row addition, while `corpus/SOURCES.md:176-177` records current historical disposition; preserving its old used-by prose is intentional history, not a current-row claim.
- No installs/updates, package transactions, service restarts, domain-target actions, production edits, delegation, Git mutations or scratch files. Only this report and its receipt were written; no scratch cleanup required.

Self-check: accuracy 4 (exact immutable bytes; no runtime semantics asserted); completeness 4 (all three payloads, sections and full scaffold covered; semantic tooling unavailable); clarity 4 (historical/current offsets separated); actionability 4 (no D5 repair needed; claim limitations explicit); conciseness 4 (full hashes retained for reproducibility). Overall 4.0; no fixable scoped omission identified.

Report: .ufo/waves/round-47/w2/R47W2D5Payload.md
