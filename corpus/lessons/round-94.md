author: kasegi (round 94, attempt 1)

# Round 94 — lesson

## Gate

Candidates this round (every row opened 2026-11-07):

| source | verdict | ground | located quote |
|---|---|---|---|
| S140 — GitLab secret-detection rules, `rules/mit/gitlab/gitlab.toml` at commit 59ada1f4 (repo `gitlab-org/security-products/secret-detection/secret-detection-rules`) | **ADMIT**, kind `code`, tier A for the GitLab token-shape scope | the vendor's own machine-readable rule for the shapes this round lands; it publishes the alphabet, the optional custom instance prefix and the length that the prose page (S139) does not | `regex = '''\b((?:[a-zA-Z0-9]{1,20}-)?glpat-[0-9a-zA-Z_\-]{20})(?:[^0-9a-zA-Z_\-]|$)'''` (capture `corpus/source-snapshots/round-94/S140.txt:4`; runner form at :114, deploy form at :255) |
| S141 — the same repository's `rules/mit/github/github.toml` at commit 59ada1f4 | **REJECT**, kind `code`, tier B at most | opened this round but not cited by an admitted entry: its `ghr_` 76-character refresh-token rule is a round-95 lead, and GitLab is not the vendor of GitHub tokens | `regex = "ghr_[0-9a-zA-Z]{76}"` (fetched file, line 72; 3955 bytes, sha256 `02c67ceb…`) |

Redaction (a capture rule, not a source-row change): the ruleset's example
arrays are published token values, and GitHub push protection refuses them as
secrets (GH013 refused the first freeze at `S140.txt:192-195` and `:394`).  The
committed snapshot therefore replaces **every** element line inside an
`examples = [` or `negativeExamples = [` array with one fixed marker (82 lines,
listed by rule id in `.ufo/waves/round-94/controls/redaction-r94.txt`).  Line
numbering is preserved, the three quoted regex lines keep their anchors, and
`corpus/instruments/source-recheck.py` re-derives all three (rc 0).  The intake
gate refused the unredacted bytes (`.ufo/waves/round-94/controls/capture-intake-r94.txt`),
and the committed bytes scan clean with no allowlist row.

Census: `.ufo/waves/round-94/controls/census-start-r94.txt` (rc 0, 139 rows,
six inherited W04 warnings) → `.ufo/waves/round-94/controls/census-mid-r94.txt`
(rc 0, 141 rows, the same six W04 warnings).  Registry deltas: S140 added
(`queued` at the freeze → `mined` at integration), S141 added (`rejected`).

Spot-check: the non-author closure (`corpus/lessons/round-94-verifier-spotcheck.md`)
samples the S140 admit and the S141 reject and records it here at closure time.

## Mistakes

| # | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| M94-1 | survivor | round-93 M93-4: the plant nonce inserted one directory but left basenames and the `round-1/` segment, so a path-shape-keyed detector passed every limb (`corpus/lessons/round-93.md` § Wave findings; `MutC2Counter` F1) | none — no limb or control keyed on path shape | `relocate()` derives every directory and basename from `sha256(nonce|path)`; the frozen forgery `F1-path-shape-keyed` fails K4 (`c2-controls-r94.txt`), and K9 forbids losing a shape the previous landing caught |
| M94-2 | vacuous | round-93 M93-5: the M3 union crashed on a labelled non-knowledge file (`b, a = file_at(...)` shadowed the argparse namespace), so the "walks every labelled file" limb could not run on the input it exists for | none — the limb had no control exercising a file outside `corpus/knowledge` | the shadowing is fixed; `m3-union-applied` passes (rc 0) and `m3-union-unmapped` fails M3 on an unmapped edit; the round-93 counter's traceback is the red-before (`c1-controls-r94.txt`) |
| M94-3 | landing | GH013 refused the first round-94 freeze: the redaction had covered only the shapes the lane's scanner knows, and GitHub's own detectors flagged five more published example lines (`S140.txt:192-195` GitLab Feed Token, `:394` Feature Flag Client Token) | none — the lane's intake gate and the redaction rule both keyed on the lane's shape list | the redaction rule is structural, not scanner-derived: every `examples`/`negativeExamples` element line is replaced, listed by rule id in the receipt; QUALITY R146 |
| M94-4 | number-drift | round-93 R145 cites "the 39 [CHANGE rows] whose base range meets the replaced docstring block" with no committed enumerator (round-93 spot-check routed defect 6); the committed enumerator prints 32 (bare tokens at their own line) or 44 (resolved to the preceding full-path range) against the diff's replaced ranges `88-89, 96, 156, 195` (`.ufo/waves/round-94/controls/r145-enumerate-r94.txt`) | R145's own clause ("a committed command") was not met at r93; no criterion checked the cited count against a command | the enumerator is committed and R147 supersedes R145's example count; R145's hand-narrow duty stands |

## Wave findings

One v1 wave, 13 seats, all settled (no dead seat); receipts under `.ufo/waves/round-94/w1/`.

- **CriticClaimsC1** — P1/P2/P3 STANDS (fresh shared clone, meter and pins re-derived); **P4 does not
  reproduce**: the before-fixture in `controls/c1-controls-r94.py` clones the mutable live lane instead of
  pinning `dff5a0a`, so after the tranche lands the `m5-cell-repair-before-r93` reception flips to
  `rc=1 want=0`, and the receipt's `candidate=e7adac6…` is a scratch commit that is not an object in the
  lane repo. The critic's one-line pin restores `C1-CONTROLS-RESULT pass controls=12`. Under the frozen kill
  rule (`P4 not reproducing: C1 NOT VERIFIED`) C1 is **NOT VERIFIED**; the substance (19 repoints, map,
  labels, EXCLUDED set, meter) is correct and re-derived. Routed: pin the before-fixture to the frozen base
  rev and record a repo-object candidate at the next freeze.
- **ExecC1Indep** — AGREE/STANDS: all 19 map rows reproduce their after lines (line 397 composes two edits),
  the changed set is exactly 18 lines (17 + 1), no other line moved, `SKILL.md` byte-identical.
- **MutC1Counter** — STANDS; 17 mutants killed, 0 survivors; seven mutants are invisible to the frozen suite
  and were killed only by the seat's own fixtures (routed coverage gaps), plus two qualifiers (R1, R2).
- **ReviewC1Labels** — C1 STANDS on P1–P3; 18/19 landed rows CORRECT, 1 PARTIAL (row 151: the pane-target
  tie, routed), 0 WRONG; 9/10 exclusions right (row 396 is token-fixable in substance). It wrote 2 round-95
  labels and a verifier (`round95-labels.tsv`, `ROUND95-LABELS-VERIFY … PASS`).
- **CriticClaimsC2** — P1, P2, P3 STANDS (K1–K9 at three seeds; pins; two-path landing; row byte-equal).
  **P4 does not stand as written**: it names `s140-allow-rows-removed`, a control the redaction made vacuous
  and which the receipt replaced with `tampered-instrument`. C2 is **NOT VERIFIED on P4 as written**; the
  capability itself is green at three seeds and all four of the seat's own forgeries die on behavioural limbs.
- **ReviewC2Scanner** — C2 STANDS on P1–P3 and on its clause-by-clause read of the scanner and S140; it reads
  P4's mismatch as a routed claim-text defect rather than a kill trigger (the receipt prints 10/10). Eight
  qualifiers (known-limits wording, the redaction’s effect on two sentences) routed.
- **MutC2Counter** — 6 of 7 forged detectors killed unpinned by behavioural limbs; one SURVIVOR (F7, a
  scanner that drops the unplanted `session-cookie` gate shape) and the P4 enumeration defect routed.
- **SentinelShapes** — C2 STANDS on the probed surface: 52 encoding and 32 boundary fixtures behave as the
  statement says; three defects (D1–D3: two credential-shaped vendor classes from S140 neither detected nor
  named; an allowlist that cannot be derived for a prefixed token in an escaped context; two provenance/limit
  sentences that need precision) and four qualifiers routed.
- **ScoutGitLabRules** — AGREE on S140: the commit-pinned fetch equals the manifest digests and the committed
  capture differs on exactly the 82 redaction-marker lines; it also records that the seat brief's "18 redacted
  lines" is wrong (82 lines across 24 rules). Three leads routed for round 95.
- **ConnectorOverlap** — 20 sibling lanes scanned: no sibling detects a length-bounded custom instance prefix,
  a runner-auth token or a deploy token; no sibling gate verifies token-level knowledge citations; no sibling
  duplicates the `capture-secret-scan` capability row. It also measured limb duplication (M1/M3, M4→M5).
- **CriticHarm** — one named harm: the C2 landing grew the scanner 458 → 491 lines and mis-pointed 65 of 102
  full-path citations into it across five entries (six verbatim quotes false). Repaired at integration (see
  below); all other harm items re-derived clean.
- **ScribeGate** — Gate/Mistakes/Census re-derived from committed evidence; S140 STANDS; the draft supplies
  the Gate and Mistakes blocks above.
- **ExecC2Probe** — AGREE on its own 14 fixtures (7 positives, 7 negatives) and the selftest.

Integration repair (R143/R144/R145/R147): every `capture-secret-scan.py:N[-M]` citation in the five entries
re-anchored from the base→tip content map (68 tokens; one hand row for the single citation inside the
rewritten docstring block, `:106-107` → `:120-121`); the CriticHarm drift table reconciles 35/35;
`anchorcheck.py` reports 0 bad on all five; receipt `.ufo/waves/round-94/l1/reanchor-r94.txt`.
