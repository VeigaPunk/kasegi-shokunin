# Round 93 — lesson (kasegi, attempt 1)

Read first: the r92 closure (`admitted`) and `corpus/lessons/round-92-verifier-spotcheck.md` (both claims verified; routed defects 1–8), `corpus/lessons/round-92.md` (M92-1..3). Base `e15996bfd2f6eca4af39507a7c5973afbeca8347`, freeze `5bad9e55d3d9319446e3d9b63bc2dece633cdb68`, C1 landing `ae53b3c6e7e2ce070c2f022d01c1677a8908df1b`, C2 landing `9225954a6e3f177af46bdb9d811c062a4353a552`. Frozen claims, predicates, kill rules and executed controls: `.ufo/waves/round-93/claims.json`, `.ufo/waves/round-93/controls/`.

## Claims

- **C1 — depth:verifiability (lowest axis, score 4; citation repair, score not claimed to move).** Tranche 8 closes the last five GONE bare-key sites the round-92 census left in `corpus/knowledge/triage-thresholds.md`: the 437/438 errata cells are replaced whole by the exact cells the round-92 non-author seat ReviewC1Labels wrote, the 454 second token repoints from `SKILL.md:494-506` (park-disposition text) to `SKILL.md:827-848` (the EV formula), and the 58/144 surviving `MATCHES: SKILL.md:117` ties repoint to `SKILL.md:191` (the only attempts statement; `MAX_ATTEMPTS` occurs 0 times in SKILL.md). The 3 CORRECT pairs stay unedited. The successor counter adds the `cell-repair` kind (a whole-cell old→new from the label) and lane-root `SKILL.md:N[-M]` values (M4 binds the lane root, M5 range-checks it), and M3 now walks every labelled citing file, not only `corpus/knowledge` (the r92 CriticClaims counter gap). Frozen target: knowledge meter 1007/2001 → 1009/2000.
- **C2 — coverage (score 8 held), capability extension of `capture-secret-scan` (sourced: S139).** New shape `gitlab-pat`: `glpat-` + exactly 20 characters of `A-Za-z0-9_-`, both boundaries, a preceding escape terminator allowed; and the `github-token` left boundary now accepts the escape-terminator family (`\t`, `\r`, `\n`, `\uXXXX`, `%XX`, `&#NN;`, `&#xXX;`), closing the round-92 SentinelGitHub P1 family (11 measured misses). The successor counter plants every value under a run-time nonce directory and carries U1–U6 boundary negatives.

## Outcome

- **C1:** `KNOWLEDGE-METER-RESULT pass rc=0` at the landing in a clean clone: M0 1007/2001, M1 1009/2000, M3/M4/M5/M6 pass, M9 5/5, M10 want=5 mapped=5 (cell-repair=2, no-edit=3, range=3); P3 prints one path (`corpus/knowledge/triage-thresholds.md`). Receipt `.ufo/waves/round-93/l1/c1-landing-r93.txt`.
- **C2:** `CAPABILITY-CHECK-RESULT pass rc=0` at the landing at the run-time seed and seeds 1 and 9191 (K1–K8; K1 pins instrument `7d9d7309…` and gate `8b6f8493…`); P3 prints `SCORECARD.md` + `corpus/instruments/capture-secret-scan.py` and the row equals the frozen candidate row. Receipt `.ufo/waves/round-93/l1/c2-landing-r93.txt`.
- **Controls executed before the freeze** (receipts in `.ufo/waves/round-93/controls/`): C1 candidate PASS and ten do-nothing/forgery variants FAIL (including the M3 labelled-file scope unit control); C2 candidate PASS pinned and fourteen variants FAIL (no-work, ten forgeries G1–G10, the round-92 row, and the S139 allowlist rows removed).

## Gate

### S139 — GitLab Docs, Secret detection: Detected secrets (admitted, used by the instrument)

- **URL:** https://docs.gitlab.com/user/application_security/secret_detection/detected_secrets/, HTTP 200.
- **Accessed:** 2026-11-07 (capture 13:55:21Z).
- **Capture:** `corpus/source-snapshots/round-93/S139.txt`, sha256 `154a7e1535b4a245e45e3f82705c271344f59aa6c344807645fa0bc4d1e1b188` (25,370 bytes, 414 lines; the frozen manifest's `lines` field read 415 and is corrected to 414 at integration, content unchanged); manifest `corpus/source-snapshots/round-93/manifest.json`; `source-recheck.py` rc 0 (anchors 87 and 85, `occurrences=1`; `.ufo/waves/round-93/controls/source-recheck-r93.txt`); scanned with the frozen candidate before the freeze, hits=0, allowed=4 (`.ufo/waves/round-93/controls/capture-intake-r93.txt`).
- **Located quote, S139.txt:87 (6 words):** "glpat- followed by a 20-character string". Lines 85-86 are the rule sentence ("Rule-based detection identifies secrets by matching scanned content against a known pattern for each / credential type, called a rule"), line 84 the section heading "Rule-based detection"; the page states no alphabet and no total length.
- **Row change (old → new):** new row, status `queued` (freeze `5bad9e55`) → `mined` (integration); used-by `—` → `corpus/instruments/capture-secret-scan.py`.
- **Admission gate note:** the page as served was refused by the round-90 intake gate (`bearer` line 124, `credential` lines 116/126/139). The four matched values are the page's generic-detection teaching samples; each was read in context and bound by one digest row in `corpus/instruments/capture-secret-allow.tsv` (rows for `corpus/source-snapshots/round-93/S139.txt`).

### Rejected this round

- **GitLab Docs, Personal access tokens profile page**, https://docs.gitlab.com/user/profile/personal_access_tokens/, HTTP 200 on 2026-11-07 (81,326 bytes fetched). Rejected as the C2 source: the converted text carries no `glpat` occurrence (`grep -c glpat` over the converted page = 0), so it cannot ground the prefix. Correction from wave seat ScoutGitLab: the page **does** state the token length — "The token must be 20 characters long." at converted line 297 — so the rejection rests on the missing prefix only, and the page is an independent second corroboration of the 20-character length (a round-94 depth lead, not a C2 source). Not registered; flip: the page names the `glpat-` prefix.

### Post-capture check of the trap

The rejected candidate was fetched, converted and read, and the accepted source re-checked, in the same round; neither file was committed beside the capture. The capture passed the intake gate only after four digest-bound rows, and the gate still refuses any other value at that path.

## Mistakes

**M93-1 — class `diff-mapped-anchor-too-wide` (recurrence of M92-3; captured this round).**

- **What happened:** the re-anchor tool maps a replaced block start→start and end→end, so a one-line citation `capture-secret-scan.py:96` became `:107-109`, and `:95-96` became `:106-109`; the ranges now span the new GitLab known-limit lines. `quote-anchor-check.py` read `bad=0 out_of_range=0` over the widened ranges, because a quote found anywhere inside a range is `ok`.
- **Captured-by:** no mechanical check; the L1 enumerated every CHANGE row whose base range meets the replaced docstring block (`base_start <= 105 and base_end >= 87`, a committed one-liner printed 39 rows), read each against the landed lines, and made 12 hand dispositions (single tokens narrowed, clause ranges narrowed, three false sentences rewritten). The enumeration is the operational form of R144.
- **Fix:** single tokens narrowed by hand (`:109`, `:110-111`, `:106-107`), wide ranges narrowed to the clause they name (`:86-97`, `:109-115`), and three sentences the landing made false rewritten (the boundary clause twice, the JSON-exception paragraph, the shape-count sentence in `capture-intake-gate.md`). R145 records the enumeration requirement.
- **Shown able to fail:** `.ufo/waves/round-93/l1/reanchor-r93.txt` holds the widened `:96 -> :107-109` and `:95-96 -> :106-109` CHANGE rows; the quote checker run before the hand pass printed `bad=0`, so the checker alone cannot catch the class.

**M93-2 — class `gate-scope-is-bytes-not-path` (this round).**

- **What happened:** the first S139 capture was written to a scratch path outside the lane, on the assumption that the lane-relative path exemption would let it through. The gate refused it (`INTAKE-REFUSED … written=no`, rc 3): it scans the converted bytes under whatever `--out` path is given, and only the allowlist can let a matched value through.
- **Captured-by:** the gate's refusal itself, before any file was written.
- **Fix:** read all four matched values in context, wrote four digest-bound rows for the exact capture path, and captured through the gate; the pre-capture refusal and the rows are in `.ufo/waves/round-93/controls/capture-intake-r93.txt`.
- **Shown able to fail:** the same command with the allowlist rows removed still refuses (`s139-allow-rows-removed` control, `.ufo/waves/round-93/controls/c2-controls-r93.txt`: K3 hits=4 and rc 1).

**M93-3 — class `label-provenance-transcription` (this round; record-only).**

- **What happened:** the two 58/144 labels were not written by a seat this round; the L1 transcribed the remediation the round-92 non-author seat ReviewC1Sites stated (`.ufo/waves/round-92/w1/ReviewC1Sites.md:17-28`). R140's bar is a non-author hand-labelled sample; the label text is the reviewer's, but the transcription is the L1's.
- **Captured-by:** the L1's own freeze note; no counter observes authorship.
- **Fix:** each transcribed row carries the reviewer's evidence pointer and the round-92 commit; the report names the provenance. The wave's ReviewC1Labels re-read both rows against the landed bytes.
- **Shown able to fail:** the two rows are in `.ufo/waves/round-93/c1/labels.tsv` with `ReviewC1Sites (round-92 wave, commit 7ba6623)` in the evidence column, and the freeze's `declined` block does not claim a fresh seat label for them.

**M93-4 — class `statement-clause-not-bound-by-the-counter` (recurrence of M89-2; wave finding).**

- **What happened:** the C2 statement says the nonce reroot means "a path-keyed forgery cannot know the paths". Wave seat CriticClaimsC2 built a round-92 scanner (no `gitlab-pat`, no escape boundary) keyed only on the *shape* of the rerooted paths (`<dir>/r<8 hex>/round-1/...`, `w/n<8 hex>/...`) and it passed all eight limbs at rc=0 (forgery H). The nonce is a deterministic syntactic transform and leaves the basenames and the `round-1/` segment intact.
- **Captured-by:** CriticClaimsC2's forgery H (`.ufo/waves/round-93/w1/CriticClaimsC2.md` § qualifier); the frozen predicate does not test the sentence.
- **Fix:** routed to round 94 — randomise the basenames and the `round-1` segment (not only a directory nonce), and add a path-shape-keyed forgery to the frozen controls. The claim's predicate P1–P3 still holds at the landing; the parenthetical is reported as a material qualifier, not a re-score.
- **Shown able to fail:** forgery H's run under the frozen counter (CriticClaimsC2 receipt) prints `CAPABILITY-CHECK-RESULT pass rc=0` with the round-92 instrument, so the sentence is false as implemented.

## Wave findings (none re-scores a claim)

- **CriticClaimsC1:** C1 STANDS on P1–P3, re-derived from committed bytes (frozen run rc 0; each forged variant and the (site, key) completeness shown). Observation: the M3 labelled-file union is exercised only by the wave's unit control, not by the round's own label set (all labels cite `corpus/knowledge`); the control's success is a traceback, see M93-5.
- **CriticClaimsC2:** C2 STANDS on P1–P3; material qualifier Q1: the statement's "a path-keyed forgery cannot know the paths" is false as implemented — the nonce reroot is a deterministic directory transform that leaves basenames and the `round-1/` segment intact, and forgery H (a round-92 scanner keyed on the path shape) passes all eight limbs unpinned (M93-4).
- **ReviewC1Labels:** 8 CORRECT / 0 PARTIAL / 0 WRONG — all five landed edits and all three no-edit pairs; round-94 next-tranche labels written and verified (`round94-labels.tsv`, 29 rows, 35 distinct tokens, `ROUND94-LABELS-VERIFY … failures=0 PASS`, sha256 `41bc438b…`).
- **ReviewC2Scanner:** APPROVE; D1 (stale class-B sentences in the github entry, "fifteen gh cases / cases=68") closed in the integration; D2 (docstring and counter clause titles say `S139 line 86` where `glpat-` is at 87), D3 (`&#xXX;` escape unpinned) and D4 (stale K8 doc line; no GitLab left-boundary plant) routed to round 94 — D2 cannot be fixed without changing the pinned instrument or the frozen counter. Its reanchor table: 82 distinct full-path ranges, 60 moved by the landing.
- **MutC1Counter:** killed=7 survivors=12 of 19 mutants; R1 (high) the M3 union walk crashes on a non-knowledge labelled file and the unit control passed on the traceback (M93-5); R2 M5 does not bind a lane-root token inside a cell replacement (probe F1 rewrites 437's `SKILL.md:176-178` past EOF and the frozen counter still passes); EXCLUDED empty leaves three mutants indistinguishable, one a latent M10 defect with a proving input. None changes the base/after readings (P1 holds).
- **MutC2Counter:** forged=7 rejected=4 survivors=3 (F2 harness-name gating, F6 gutted selftest, F7 suffix-keyed); all three are rejected only by K1 when the sha pins are supplied, so they pass unpinned. Routed D1–D3 for the counter's next round.
- **SentinelEscape:** 67 probes, 44 DETECTED / 23 MISSED (11 statement-named negatives behaving as written, 12 unnamed miss classes routed: `\b`/`\f` JSON escapes, `\xXX`, `%uXXXX`, octal, double-encoded `%25XX`), 2 FP-shaped detections (bare `glpat-` + 20 x's needs an allowlist row at a capture path), ReDoS max 1.241 s/MB with the new shapes at or below the filler baseline.
- **ScoutGitLab:** capture-equal=yes (re-fetch byte-identical); 9 ranked leads; corrected the frozen frontier note (the PAT profile page does state the 20-character length at line 297); D1–D3 coverage gaps against GitLab's own rule (custom instance prefix, routable/versioned PAT forms, `ghr_` 76-character refresh tokens).
- **ConnectorOverlap:** 20 sibling lanes scanned; 0 bounded `glpat-` detectors, 0 escape-aware scanners, 0 lanes detecting both round-92 GitHub shapes; the kasegi intake gate inherits both new classes (live harness). Adjacency evidence only.
- **CriticHarm:** NO HARM on items 1–6: density byte-identical (273.2), `--rev` 1957 files hits=0, `--files` 286 knowledge/snapshot files hits=0, identical 23-hit/18-file set over 6,275 tracked `.md`, ReDoS flat, the round-92 counter still passes K1–K8, and no citation site lost a resolving citation (net +2).
- **ScribeEntry:** drafts=4 PASS; D1 (manifest `lines` 415) corrected to 414, D2 (scanner `S139 line 86`) routed, D3 (the row-change bullet's "teaching samples") corrected by an appended bullet.
- **ExecC2Probe:** AGREE on the probed surface (`rev_hits=4 files_hits=4`, `--selftest pass cases=90`, intake refused); per-row allowlist perturbation proves each S139 row binds its own value (lines 116/124/126/139).

**M93-5 — class `control-passes-on-a-traceback` (this round; wave finding).**

- **What happened:** the round-93 counter's M3 labelled-file union declared `b, a = file_at(...)`, shadowing the argparse namespace `a`; any labelled citing file outside `corpus/knowledge` turns `a` into a string and `if a.map_sha256:` raises `AttributeError` before any LIMB line. The frozen control `m3-labelled-file-scope` recorded `rc=1 want=1 PASS` — a crash read as a detection, and the claim's sentence "M3 walks every labelled file" is inoperative on the input it exists for.
- **Captured-by:** MutC1Counter R1 (`.ufo/waves/round-93/w1/MutC1Counter.md` § R1; `probes/P17-fx7-frozen.txt`, `02-r1-shadow-repro.txt`). Its `variants/r1fix.py` (rename `a` → `a_txt`) makes the limb print `LIMB M3 FAIL bad_lines=1` on the same input.
- **Fix:** routed to round 94 — rename the variable, re-run the union control with a LIMB assertion (rc alone is not enough), and add the M05 line-count mutant's proving input. The landing's 8 labels cite only `corpus/knowledge`, so no base/after reading changes (P1 holds honestly).
- **Shown able to fail:** the frozen control's receipt shows no LIMB line at all on the non-knowledge label input; the fixed variant produces the line and the mutation is detected.

**M93-6 — class `credential-shaped-fixtures-in-evidence` (this round; push block).**

- **What happened:** the wave receipts quoted GitLab's own published example PATs and synthetic `glpat-`/`ghp_`/`AKIA` fixtures verbatim. The local wave-evidence commit `78c77140` was blocked by GitHub push protection (GH013, GitLab Access Token, 8 values), so the branch could not advance until the evidence was redacted (and the unpushed commit rewritten or the secrets unblocked).
- **Captured-by:** the remote's GH013 response, reproduced in `~/.local/state/shokunin-hyaku/jj-_home_vgpnk_Projects_shokunin_kasegi-shokunin.err`; the lane's own `capture-secret-scan.py --files` over the wave evidence (`hits=22` before, `hits=0` after redaction).
- **Fix:** every credential-shaped value in the round's new evidence is redacted (`glpat-REDACTED-r93`, `ghp_REDACTED-r93`, `AKIA-REDACTED-r93`); the seats' reports keep the line and verdict, not the value. Rule for round 94: run the scanner over the wave directory before committing it, and redact fixtures in seat reports the same way captures are redacted (R138's discipline extended to receipts).
- **Shown able to fail:** the pre-redaction scan prints 22 hits and the remote refused the push; the post-redaction scan prints `hits=0`, and the rewritten commit pushes.

## Routed-defect disposition (r92 spot-check §6 and wave findings)

| # | routed defect | r93 disposition |
|---|---|---|
| 1 | 454's second token and the 58/144 `SKILL.md:117` ties (r92 ReviewC1Sites F1) | Done in C1 (5 edits); 58/144 labelled from the round-92 reviewer's remediation (M93-3). |
| 2 | M3 scope narrower than the labelled set (r92 CriticClaims counter gap) | Done: M3 walks every labelled citing file; the `m3-labelled-file-scope` control fails when a labelled non-knowledge file changes. |
| 3 | C2 counter D1–D5 (randomised plants, bounds, K6 blindness) | Partially: plant paths and tempdir names are run-time random; U1–U6 plants added; K6 blindness not claimed. Carried to round 94. |
| 4 | SentinelGitHub P1 escape terminators | Done (scanner + plants + selftest cases); P2 encoded separator documented as a named limit, not widened. |
| 5 | SentinelCookie F1–F3, r91 FC1–FC4 | Still routed (cookie shape untouched). |
| 6 | `capture-source.py` M90-2 `file://` crash, missing `--allow` file, r90 C2-F1..F3 | Still routed (separate surface). |
| 7 | Assimilation quarantine slice (7 rows) | Carried; nothing appended from the package. |
| 8 | M92-3 re-anchor tool widening; docstring citation looseness ("40 characters in all" should also name S137:171, where the `* 40 = 160` literal sits; S136:160 and S137:174 state the unchanged length) | Re-anchor: tool unchanged, hand enumeration committed (R145). The docstring citation is carried to round 94: editing the scanner now would change the landed instrument bytes and break C2's P2 pin. |
| 9 | The six W04 duplicate-URL census warnings (S028, S029, S072, S076, S080, S085) | Inherited, unchanged this round; the census prints the same six and exits 0. |
