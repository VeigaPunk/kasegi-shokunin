# R48Review01 — Canonical seed vs restored SHONEN.md: byte-equivalence review

Seat: R48Review01 (reviewer, leaf). Claim under review: C1 (routed-defect closure, axis depth:verifiability).
Probe (bounded, author-side): check the canonical source seed mechanically against the restored
`SHONEN.md`, normalizing only permitted marks/evidence lines; prove or refute byte-equivalence.
No production file, fleet file, sibling, domain tree, or git/jj state was touched. Scratch:
`/fast/scratch/hyaku/kasegi-r48/R48Review01/` (created, used, removed on exit after this report saved).

Round-47 routes read: `corpus/lessons/round-47-verifier-spotcheck.md` §6 — **R1** (SHONEN.md
canonical-form drift: 13 accumulated per-round assessment blocks / 52 `[~]` lines; route = restore
toward canonical seed shape) and **R2** (plain-target phrasing; contextual only, not this probe's axis).
Normative seed source: `.ufo/waves/round-48/controls/protocol-source.txt` (S077 snapshot), file-contract
paragraph "Verification is mechanical".

## Verdict

**Byte-equivalence PROVEN.** After normalizing only the permitted variation — the box mark character
(` `/`~`/`x`) and at most one indented `Evidence:` line per box — the restored
`/home/vgpnk/Projects/shokunin/kasegi-shokunin/SHONEN.md` is byte-identical to the canonical seed
extracted from `protocol-source.txt` with `<name>` → `kasegi-shokunin`.

- Normalized seed sha256:    `890223902c4c771a60ef454e8ccbe16546e88d5580cf0b3349036bda05025e18`
- Normalized restored sha256: `890223902c4c771a60ef454e8ccbe16546e88d5580cf0b3349036bda05025e18` (equal)

## Method and exact commands

1. Seed extraction + normalization + comparison, fixture driver at
   `/fast/scratch/hyaku/kasegi-r48/R48Review01/verify-seed-equivalence.py` (removed with scratch):

   - Extracted the indented seed block following the heading
     ``The canonical `SHONEN.md` seed (verbatim — `<name>` is the only substitution):`` from
     `controls/protocol-source.txt`; the trailing un-indented `Marks: …` paragraph is protocol prose,
     not seed (the block's 4-space indentation ends before it; the frozen checker's grammar likewise
     ends at the last box/evidence line — anything further is `SF-TRAILING`).
   - Substituted `<name>` → `kasegi-shokunin` (the only permitted substitution).
   - Normalized the restored file: each `- [<mark>] <label>` → `- [ ] <label>`; each single
     `      Evidence: …` line dropped; all other bytes untouched.
   - Result: 8-line normalized forms identical; `diff` empty; exit 0.

2. Frozen counter at the final measured tree:

   ```
   $ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/shonen-form.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin
   shonen-form canonical=1 finding=SF-CLEAN exit=0    (counter-exit=0)
   ```
   Expected (claims.json `expect_after`): `shonen-form canonical=1 finding=SF-CLEAN exit=0` — **match**.

3. Byte-hygiene audit of restored `SHONEN.md` (761 bytes, 12 lines): LF-only (no CR), single trailing
   newline, no tabs; heading em-dash is U+2014 (`e2 80 94`) byte-equal to the seed's; 4 box lines,
   4 evidence lines, no other prose.

4. Normalization delta inventory (proves only permitted lines varied): marks on lines 5/7/9/11 are
   `~`, ` `, `~`, `~` → all normalized to `[ ]`; exactly 4 evidence lines dropped. No box added,
   removed, reordered, or relabeled; no other prose added or deleted.

5. Evidence-pointer resolution (mechanical existence only, per claim `mechanical_limits`): all four
   pointers resolve, are repo-relative, and stay inside the root —
   `SKILL.md`, `LOG.md`, `corpus/lessons/round-47-verifier-spotcheck.md`, `PROVINCE.md` (each
   `is_file()` true, `is_relative_to(root)` true).

6. Kill-rule archive retention:
   `sha256sum .ufo/waves/round-48/controls/shonen-before.txt` →
   `596122c0f6b598d49eeb384898dc124d41ddb4ea867a569d77402d83017e9c05` — **equal** to the kill rule's
   required archive digest; historical round-47 bytes retained.

7. Frozen counter + frozen fixtures replay: `corpus/instruments/shonen-form.py`
   sha256 `0ab32a2c6155a7d0055196df806898cb7e78880a072bf2504143b99377b313dd`; all 17 cases in
   `controls/fixtures.json` re-run through the counter with pointer resolution anchored at the lane
   root (`--root <lane> --file <fixture>`) reproduce `controls/pre-freeze-fixtures.txt` exactly —
   17/17 expected exit+finding, 0 mismatches. The `canonical` fixture text is byte-identical to
   `controls/canonical-candidate.txt`.

## Expected vs observed

| Check | Expected | Observed | Match |
|---|---|---|---|
| Seed vs restored, normalized | byte-equal or refuted | byte-equal (sha256 equal) | yes |
| Frozen counter on lane root (`expect_after`) | `canonical=1 finding=SF-CLEAN exit=0` | `canonical=1 finding=SF-CLEAN exit=0` | yes |
| Archive SHA256 retention | `596122c0…17e9c05` | `596122c0…17e9c05` | yes |
| 17-case frozen fixture replay | per `pre-freeze-fixtures.txt` | 17/17 exact | yes |

## Restored file vs integrated candidate (informational, no defect)

`diff controls/canonical-candidate.txt SHONEN.md` differs only in (a) four evidence-line texts
(candidate repeats `LOG.md — Author assessment only; no promotion claimed.`) and (b) box 2's mark:
candidate `[~]` vs restored `[ ]`. Both forms are inside the permitted normalization envelope; the
restored file is the more conservative one — box 2 (end-to-end domain task) stays unchecked because no
end-to-end task is claimed, matching the round-47 spotcheck §6 operator note. Author-side form only;
no promotion or semantic truth is asserted or implied by this review.

## Findings

No actionable defect. C1's restoration limb (R1) verifies mechanically at the current tree: canonical
form restored, historical bytes archived at the required digest, frozen counter green at
`expect_after`, kill-rule limbs intact (no hidden/commented/duplicate checklist passes the frozen
checker — the 17-case fixture replay includes fenced/commented/duplicate/extra-prose negatives, all
still rejected; `x`-mark rejection is enforced by the frozen `SF-VERIFIER` limb).

## Residual risk and verification gaps

- **Frozen-id form:** the assignment header's frozen id `3546f7089c224ac6c8adc68208b1e648bbf3e6a5`
  (40 hex) matches no common digest of `claims.json` bytes (tried sha256 raw/compact/sorted-compact,
  sha1, blake2b-20). The on-disk freeze record `freeze.txt` pins
  `claims-sha256: b8022cdf4d4bfa8efb0dabc807318e02a66d1ab1101b726a20f1f31c69f2a345`, which is exactly
  the measured sha256 of the file; the claim was verified from those bytes. The 40-hex id appears in
  `wave1-spec.json`/`wave1-dispatch.json` and is treated as an orchestrator-internal identifier.
- **LSP unavailability:** no `lsp` device is mounted in this session's tool inventory; caller/definition
  checks were performed by executing the one canonical runtime directly (the frozen counter) and by
  byte comparison, not text-grep inference.
- **Out of scope, not re-run:** the 6-mutant pre-freeze battery (`controls/pre-freeze-mutants.txt`,
  6/6 caught at freeze) belongs to sibling probe seats; pointer *semantic* truth and promotion remain
  independently judged per the claim's own limits.
