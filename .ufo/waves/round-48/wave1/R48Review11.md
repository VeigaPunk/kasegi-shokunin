# R48Review11 — Connector: R1/R2 lineage into R41/R48/R50/R53; contradictions in R55

- **Seat:** R48Review11 (connector, leaf; no subagent dispatch, no production edits)
- **Round:** 48, wave 1 · **Lane:** kasegi-shokunin · **Axis:** depth:verifiability
- **Target claim:** C1 (canonical four-box author-assessment grammar; frozen checker `corpus/instruments/shonen-form.py`)
- **Task:** connect the R1/R2 lessons to R41/R48/R50/R53; identify contradictions in R55; no new claims
- **Date:** 2026-10-30

## Verdict

The connection holds end to end: the two round-47 non-author spot-check routes R1/R2 (`corpus/lessons/round-47-verifier-spotcheck.md:85-86`) are the direct triggers of R55's two sentences, and the frozen round-48 repair operationalizes R41/R48/R50/R53 exactly as those rules prescribe — verified by replaying the frozen counter (after-value on the live tree, before-value on the archived drift fixture). R55 itself carries **four evidence-backed tensions**: a reflexive token collision in its own grounding cell, a width mismatch between "permitted marks" and the operationalizing checker, a dropped "indented" against its normative source, and an unresolved collision with R6 through the live `considerthese` ledger pointer. None defeats C1; all are named for the integrator and the sibling critics already attacking them.

## 1. Disambiguating "R1/R2" (two senses, both load-bearing)

The tokens R1/R2 name **two distinct committed things**, and R55's grounding cell is itself the collision site:

| Sense | Location | Content |
|---|---|---|
| QUALITY rules R1/R2 | `corpus/QUALITY.md:35-36` (rows) | R1: live-claims carry as-of date + `test -e`; R2: self-description cites its counting command. Grounded in M10/M11 (`corpus/lessons/round-20-recensus.md` via `corpus/lessons/round-22.md:22-23`). |
| Spot-check routes R1/R2 | `corpus/lessons/round-47-verifier-spotcheck.md:85-86` (prose bullets under "Routed defects") | R1: SHONEN.md canonical-form drift (13 blocks, 52 `- [~]` lines). R2: `supersedes S074` plain target matches 2 lines. |

("Lessons of rounds 1 and 2" is not a live reading: round 2 has no lesson — M14, `corpus/QUALITY.md:39`.)

Enumeration run (R55's own discipline): `grep -n '\bR1\b' corpus/QUALITY.md` prints 6 matches — lines 35, 44, 249, 307, 323, **407**; `\bR2\b` matches lines 36, 226, 323, **407**. Line 407 is R55's grounding cell. A bare "R1" frozen target is ambiguous on its face; only the qualifier "round-47 non-author spot-check" disambiguates — see contradiction (a).

## 2. The connection: R1/R2 → R41 → R48 → R50 → R53 → R55

The lineage is cumulative-mechanical; each row exists because the previous one's mechanism was insufficient, and the round-48 wave is that chain operationalized:

1. **QUALITY R1/R2 (round-20 vintage)** — evidence must be dated/resolving (R1) and a self-describing artifact must cite the command that produced it (R2). Descendants make that checkable: R41 (the counter prints the token it read and the near-token it rejected), R43/R44/R47 (replay at base / do-nothing before data), R50 (mutant battery before freeze), R53 (false-green trees must read red at freeze bytes), R55 (enumerate matches before freezing). C1's evidence chain honors R1: every pointer I exercised resolves in-tree — `controls/shonen-before.txt` (sha256 `596122c0f6b5…17e9c05`, verified = the kill-rule's archive SHA), `controls/protocol-source.txt:446`, `corpus/SOURCES.md:82,177`, the spot-check file itself.

2. **Spot-check R1 (SHONEN drift) → R55 sentence 2 + R48.** M48-1 (`corpus/lessons/round-48.md`) fixes by restoring the four-box seed with one evidence line per box; historical bytes archived. R48 (content-bound limbs, `corpus/QUALITY.md:381`) is why the kill rule's second clause tests *hidden/commented/duplicate* checklists passing the frozen checker, and why the wave's 32 box-mutant probes (indent-as-code, HTML-comment, duplicate, Unicode lookalike, label byte, removal) exist. Verified counts: drift fixture = 356 lines / 52 `- [~]` lines (matches the claims' before-cell and the spot-check count exactly); current tree = 12 lines / 4 boxes.

3. **Spot-check R2 (plain target) → R55 sentence 1 + R41.** Reproduced: `grep -n 'supersedes S074' corpus/SOURCES.md` → exactly 2 matches — the S076 **row** at `:82` and the Registry-changes **prose bullet** at `:177`. M48-2 records that "R41 whole-token rule was insufficient to distinguish rows": R41's both-end literal anchoring (`corpus/QUALITY.md:353`, mechanism in `corpus/instruments/r41-closure.sh:443-459`) still matches the prose bullet because the bullet carries the whole token `S074` with clean boundaries. R55 adds what R41 cannot: the **table-row shape** anchor (`^\| S[0-9]+ \|.*supersedes`, the spot-check's own suggested fix at `:86`) plus pre-freeze match enumeration.

4. **R50 → the pre-freeze receipts.** `controls/pre-freeze-fixtures.txt` carries the 17-case battery (canonical green + 16 reds: fenced, commented, duplicate, extra-prose, crlf, no-newline, wrong-label-0/1, missing-evidence-0…); `controls/pre-freeze-mutants.txt` carries 6 single-edit source mutants, all `caught=1`. Survivor disclosure: the claims' `mechanical_limits` names the x-mark rejection and the 17+6 finiteness — R50's "closed or disclosed" clause satisfied on its face (R48Review07/08 independently verify).

5. **R53 → the wave shape.** Both attack classes at the freeze bytes: class 1 (counter mutants — the 6 in `pre-freeze-mutants.txt`, replayed by R48Review08) and class 2 (tree-level false-green probes — the 32 box/pointer probes plus the pointer-traversal reviews, each a tree that keeps markers and breaks bound content).

6. **R47 do-nothing ordering, confirmed live.** `controls/do-nothing.txt` records `shonen-form canonical=0 finding=SF-PREAMBLE exit=1`; my replay reproduces both declared values byte-for-byte (§4). R47 is what makes C1's before→after measurable at all.

## 3. Contradictions in R55 (stated, not smoothed)

**(a) R55's grounding cell fails R55's own first sentence.** R55 demands that a frozen target "anchor the table-row shape and whole identifier cells, not a phrase also found in prose. Enumerate the matches before freezing." Its own grounding cites "round-47 non-author spot-check R1/R2" — bare tokens that also name QUALITY rows `:35-36` and appear in 4–5 other cells (enumeration in §1). The routes it means are prose bullets, not rows; nothing is enumerated. The pointer resolves only via its qualifier, which is the prose-disambiguation R55 exists to replace. Reflexive, cosmetic, but real.

**(b) "Permitted marks" is wider than the checker that operationalizes R55.** R55 sentence 2: "canonical seed plus permitted marks." The normative mark set includes `[x] <verifier-id>` (`protocol-source.txt:446`). The frozen checker parses `[x]` in its box regex but returns `SF-VERIFIER` (`shonen-form.py:38-39`: "This author-side checker cannot attest independence"). So a checklist carrying a protocol-legitimate `[x]` can never read `SF-CLEAN`. Managed — the claim's `mechanical_limits` and the round-48 lesson Limits disclose exactly this under R50's disclosure clause — but R55-as-normative and R55-as-operationalized are different widths, and any later gate that grades "R55 satisfied" off `canonical=1` alone overclaims. (Corroborates the axis R48Review23 is attacking; the predicate's own "author-assessment grammar" wording already narrows scope honestly.)

**(c) "One evidence line per box" drops the protocol's "indented".** `protocol-source.txt:446`: "marks are confined to the box character plus one **indented** evidence line per box"; the checker's evidence literal is 6-space-indented `      Evidence: ` (`shonen-form.py:28`). R55's shorter sentence would admit an unindented evidence line that both the protocol's canonical form and the frozen checker reject. Precision drift between R55 and its own S077 source — the exact phrase-looseness class R55 polices.

**(d) R55's repair collides with R6 via one live ledger pointer — unresolved.** R6 (`corpus/QUALITY.md:39`): an edit to a line-cited file keeps cited lines at their numbers. Restoring the seed replaced 356 lines with 12; committed records still anchor the old layout. Most citing records are historical (round-31/33/34/37/38 lessons, `wave2/CritCalibration.md:82`) and resolve against the sha256-pinned archive. But `corpus/knowledge/considerthese-proposals-ledger.md:55` is a **live open row** citing "`SHONEN.md:164-165` box 2 `[~]`" — the restored box 2 sits at line 7 and is marked `[ ]`. Pointer and stated mark are both stale the moment the repair lands; the same ledger's round-42 row (`:139`, `SHONEN.md:249-256`) is stale likewise. No seat in this wave owns that append (corrections append, never rewrite — R5/R22 lineage). Named as debt for the integrator; I did not re-run `anchorcheck.py` to measure the blast radius, so this is a static finding over `grep -rn 'SHONEN.md:[0-9]'`, not a gate verdict.

Scope note, not a contradiction: R55 sentence 1 governs *plain-expression* frozen targets; C1's counter is a structured instrument, so sentence 1 does not apply to C1 itself — it applies to the next lane that freezes a plain target (e.g. anything shaped like `supersedes S074`).

## 4. Bounded probes executed (verbatim)

Authorized bounded probe = replay of the frozen counter; everything else is read-only hashing/grep/diff. No installs. No production, fleet, sibling, or git/jj mutations.

```text
$ python3 corpus/instruments/shonen-form.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin
shonen-form canonical=1 finding=SF-CLEAN exit=0
exit=0
$ python3 corpus/instruments/shonen-form.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin \
    --file /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-48/controls/shonen-before.txt
shonen-form canonical=0 finding=SF-PREAMBLE exit=1
exit=1
```

Expected vs observed: after `canonical=1 finding=SF-CLEAN exit=0` — observed, matches `claims.json expect_after`. Before `canonical=0 finding=SF-PREAMBLE exit=1` — observed, matches `expect_before` and `controls/do-nothing.txt`. Corroborating measurements: `sha256sum controls/shonen-before.txt` → `596122c0f6b598d49eeb384898dc124d41ddb4ea867a569d77402d83017e9c05` (= kill-rule archive SHA); `wc -l` → 356; `grep -c '^\- \[~\] '` → 52. Tree SHONEN.md sha256 `b1352168…a034a46d0`, checker sha256 `0ab32a2c…77b313dd` (same checker hash R48Probe11 observed). Current tree differs from `controls/canonical-candidate.txt` only in evidence lines and box 2's honest `[ ]` ("No new end-to-end domain task claimed") — consistent with the spot-check's §6 note that box 2 has no executed item; both forms grade `SF-CLEAN`. All four evidence pointers on the live boxes resolve mechanically (existence only, per the predicate — no semantic truth claimed). LOG.md carries the activity entry at `:2045`.

## 5. Boundaries

No new claims: every statement above quotes committed bytes or a command output printed in this session (full receipt list: `grep`, `sha256sum`, `wc`, `diff`, `awk`, and the two counter invocations). Scratch fixtures: none needed beyond read-only copies already under `controls/`; session receipts saved at `/fast/scratch/hyaku/kasegi-r48/R48Review11/receipts.txt` and removed on exit per seat spec. Form-repair support only — nothing here is promotion, semantic evidence verification, or an executed domain task.
