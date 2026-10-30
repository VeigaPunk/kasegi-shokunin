# R47RevD5 — scoped landing review

Axes: depth:verifiability; coverage. Recommendation only; no admission/integration judgment.

## Findings by severity

**MEDIUM — required line-drift note does not name affected citing files.** `R47SrD5Diff.md:128-131` names only SOURCES.md and unspecified “downstream seats”, not the files required by this seat's contract. Name the affected owners explicitly and distinguish historical evidence from live pointers. Concrete owner: `corpus/lessons/round-46-verifier-spotcheck.md:179-182` describes the old scaffold locations. Existing historical anchor-drift owners include `corpus/lessons/round-29.md:277-284`, `corpus/lessons/round-29-verifier-spotcheck.md:74`, `corpus/lessons/round-31.md:107`, `corpus/lessons/round-33.md:93`, `corpus/lessons/round-34.md:495-498`, and `SCORECARD.md:1239,1397`. The combined patch inserts two registry rows and unwraps the scaffold; offsets are not uniformly −10. Preserve historical citations rather than silently rewriting them. The F29 bullet's embedded :74/:157 belong to its explicitly named `04af9bc...` export. `corpus/lessons/round-35.md:189` cites kake's SOURCES.md:255, not this lane; it is not an affected lane pointer. Requested fix: file-named drift inventory/qualification in the landing note, with final offsets remeasured by L1 after integration.

**LOW — stale line number in the proposal's placement explanation.** `R47SrD5Diff.md:23` labels the preceding F28 bullet “(:111)” while describing the combined patched tree. Independent byte inspection places F28 at :113, F29 at :115 and Leads at :117. This is report prose only; the actual patch placement is correct. Change the prose to `base :111 → patched :113`.

No D5 landing-byte deviation found in the reviewed proposal. Both findings were sent directly to R47SrD5Diff; this report records the reviewed generation, not an assumed later repair.

## Independent evidence

Inputs: immutable `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin show fc8e0af27fbfa13220cd245700e9cb7e5e94dfc8:corpus/SOURCES.md`; `R47ScoutScaffold.md`; `R47SrD5Diff.md`; `R47SrD5Diff.draft/{R47SrD5Diff.diff,patched-SOURCES.md}` (all wave-relative paths below `.ufo/waves/round-47/w1/`). Used Python in-memory byte comparisons; parsed unified hunks, asserted each context/deleted byte line against base, reconstructed result, compared with supplied patched bytes. No fixture/runtime or counter run.

Printed results:

```
base bytes=124448 lines=185 sha256=e3bdefcfaad97e093a2950af37e62430635f130d9ea2d43fb1585db988077a6c
diff application matches proposed: True
patched sha256=a328e9cafa04b2fca9f1e8f0235ab23b856ac84cf6407694442cfb7ae6a9c16d
base payload 122 byte-equal proposed locations [115]
base payload 183 byte-equal proposed locations [170]
base payload 184 byte-equal proposed locations [171]
fences 0
EOF last two lines exactly base bullets: True
F28 line 113
F29 surroundings blank True True
```

Payload SHA256 values, including LF, independently reproduced:

| Base → proposed line | SHA256 |
|---|---|
| 122 → 115 | `9d45acb40b2061aad660306919ca8d0f073231d81dc484d3ebf9052737e6ffdf` |
| 183 → 170 | `374d7d75291d5062b69f2bc6e1afe5cfb0faee03a66deec66b6128424d2b9ada` |
| 184 → 171 | `94c88984da5448fd3d95621fefd58cf32b181d8245984694d0e9245ceaf6d198` |

Each payload occurs exactly once, byte-verbatim. The Scout's three full payload blocks also compare byte-identically to base. Search-log heading :93 < F29 :115 < Leads :117; Registry heading :124 < both final bullets :170/:171 = EOF. One blank line separates F28/F29 and F29/Leads. Full deleted prose includes all wrapped lines, not just four sentinel phrases: base :113, :115-119, :177, :179-180 (nine physical prose lines; four logical units), plus formatting/fences. Every tested instruction continuation (`blank line. PRISMA-style`, `are the ones this seat re-ran`, `established by the absence-scout`, `Follow the S073 bullet`) has zero residual occurrences. Both fence pairs are wholly removed.

Named do-nothing control: unchanged base SOURCES.md at fc8e0af. Independent comparison prints `scaffold_types=4 fence_lines=4`; independently derived D5-only deletion oracle prints `scaffold_types=0 fence_lines=0`, removes exactly 725 bytes/17 lines, and hashes to `3eb1daa507a037950520317b0248108d7265db3634f850d40253b390223e3e20`. The combined proposed result differs additionally by two registry rows, S074 cell changes and one REST-API lead; those explain its different hash and offsets. This is not a full C1 counter result.

## Residual risk / verification gaps

- Reviewed proposal bytes only; L1 must check the integrated tree preserves them after concurrent landings. No full battery, integrated counter, live-source check, or admission verification run here.
- `read xd://lsp` returned `No such tool`; no mounted semantic server/status/references/definition/diagnostics available. Literal grep was fallback evidence only, not semantic-reference proof. Drift inventory examples above are not an exhaustive semantic citation graph.
- S074 rejection/capture-binding conflict is disclosed at `R47SrD5Diff.md:135` and belongs to D7 owners; this review does not certify that concurrent behavior. Resume/routing/runtime contracts are outside this document-only D5 slice.
- Known mutation gaps remain: C1 16 uncaught and C2 18 uncaught, as assignment disclosed; no saturation/equivalence claim.
- No production/index changes, installs, delegation, background jobs, scratch directory or fixtures. Therefore no scratch remains to remove.

Self-evaluation: accuracy 4 (byte evidence strong; final integrated offsets unobserved); completeness 4 (requested D5 checks covered; semantic citation graph unavailable); clarity 4 (separates prose findings from correct landed bytes); actionability 4 (two exact report edits identified); conciseness 4 (full hashes retained for reproducibility). Overall 4.0. Main should recheck final named drift inventory and integrated payload/section invariants.

Report: .ufo/waves/round-47/w1/R47RevD5.md

## Post-review disposition

R47SrD5Diff subsequently reported both documentation findings repaired: table (a) now distinguishes base :111 → patched :113 for F28; the drift note now explicitly names `round-46-verifier-spotcheck.md:179-182` and the historical `round-29.md` / `round-29-verifier-spotcheck.md` :83 trail, without rewriting historical citations. Peer reports landing bytes/diff unchanged at `a328e9ca…`. Both findings are **resolved by author report**, not independently re-read; no actionable D5 finding remains on that reported generation. The proposal-only/integration and unavailable-LSP limitations above remain.
