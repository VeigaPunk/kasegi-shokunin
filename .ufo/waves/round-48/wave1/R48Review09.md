# R48Review09 — C1 kill-rule attack and causality: do-nothing + marker-only controls

- **Seat:** R48Review09 (critic/UFO-FSD review, leaf member; no subagent dispatch, no production edits, no commit/push, no target testing)
- **Round:** 48, wave 1 · **Lane:** kasegi-shokunin · **Axis:** depth:verifiability
- **Target claim:** C1 (canonical four-box author-assessment grammar; frozen checker `corpus/instruments/shonen-form.py`; kill rule attacked directly)
- **Date:** 2026-10-30
- **Report path:** `.ufo/waves/round-48/wave1/R48Review09.md` (relative to `/home/vgpnk/Projects/shokunin/kasegi-shokunin`)
- Read `/home/vgpnk/.omp/agent/RULES.md` first (tooling directive noted). **Tool installs:** none needed, none performed; no pacman transactions.

## Verdict

**The frozen C1 claim survives the attack.** All four kill-rule limbs hold at the measured revisions; all 24 attack variants in Sections 3–4 are caught by the frozen checker. The strongest available counterexample — a **do-nothing marker-only checklist passes the frozen checker** — is real but does **not** trigger the kill rule: it is inside the claim's disclosed `mechanical_limits` ("Evidence pointer existence is checked, not semantic truth"), and the claim's predicate describes the realized after-state, not every input that could pass the grammar. It is a **disclosed tradeoff**, not a fixable defect: the smallest safe correction is documentation-only; any checker amendment would be barred from retro-validating this frozen claim by the kill rule's own fourth limb.

## Frozen references (verified before probing)

- Freeze commit `3546f7089c224ac6c8adc68208b1e648bbf3e6a5` = `3546f70 round-48: freeze canonical checklist restoration and controls` (read-only `git cat-file`/`git log`).
- `.ufo/waves/round-48/freeze.txt`: `frozen-at: 2026-10-30T14:30:48.968093Z`, `claims-sha256: b8022cdf…`; observed `sha256sum .ufo/waves/round-48/claims.json` = `b8022cdf4d4bfa8efb0dabc807318e02a66d1ab1101b726a20f1f31c69f2a345` — **match**.
- Frozen counter bytes: checker at `3546f70` sha256 = checker at HEAD `3d7e042` sha256 = **`0ab32a2c6155a7d0055196df806898cb7e78880a072bf2504143b99377b313dd`** — no checker source amendment between freeze and HEAD, so the kill rule's fourth limb ("a checker source amendment after seat scoring cannot validate this frozen claim") is not implicated. The checker did not exist at base `903d47e` (round-48 instrument, added pre-freeze).
- SHONEN.md: base `903d47e` = `596122c0f6b598d49eeb384898dc124d41ddb4ea867a569d77402d83017e9c05` (= kill-rule archive hash = `controls/shonen-before.txt`, byte-equal); HEAD `3d7e042` = `b1352168dd7322e73f7ab2ff3e4793c77084845305d1b3a9a9e6a94a034a46d0`; worktree SHONEN.md == HEAD SHONEN.md (no uncommitted drift).
- Interpreter: Python 3.14.8. All probe trees under scratch `/fast/scratch/hyaku/kasegi-r48/R48Review09/` only.

## Section 1 — do-nothing controls at both frozen revisions (counter_cmd form)

Frozen checker exported to scratch (`checker-frozen.py`, sha above); trees built with `git show <rev>:<path>` for the 5 files `measure.py` exports (`SHONEN.md LOG.md SKILL.md PROVINCE.md corpus/lessons/round-47-verifier-spotcheck.md`); run as `python3 checker-frozen.py --root <tree>` (the frozen counter_cmd form).

```text
$ python3 checker-frozen.py --root trees/before-base
shonen-form canonical=0 finding=SF-PREAMBLE exit=1     # expect_before MATCH
$ python3 checker-frozen.py --root trees/after-head
shonen-form canonical=1 finding=SF-CLEAN exit=0        # expect_after MATCH
```

Lane harness replicated (bounded probe, explicitly authorized): `python3 .ufo/waves/round-48/measure.py --root <lane> --base 903d47e… --after 3d7e042… --work <scratch>` printed `frozen-counter-sha256: 0ab32a2c…`, `before: …SF-PREAMBLE exit=1` (`boxes: 52`, `checklist_sha256: 596122c0…`), `after: …SF-CLEAN exit=0` (`boxes: 4`, `checklist_sha256: b1352168…`) — **both claim expectations reproduce**, and the drifted mark count (52) matches the claim's `before` description.

## Section 2 — marker-only / do-nothing controls (the causality attack)

These are the strongest counterexamples available from local evidence; both **pass** the frozen checker:

```text
CASE marker-no-evidence:  exact preamble + 4 × `- [ ] <label>` + ZERO evidence lines
  observed: shonen-form canonical=1 finding=SF-CLEAN exit=0
CASE marker-empty-evidence: 4 × `- [ ] <label>` + `Evidence: EMPTY.md — …` where EMPTY.md is 0 bytes
  observed: shonen-form canonical=1 finding=SF-CLEAN exit=0  (stable after truncating target to 0 bytes)
```

**Counterexample:** a contentless marker checklist — four unchecked boxes with no evidence at all — reads byte-identical in verdict to the restored canonical checklist. The frozen counter's `canonical=1 SF-CLEAN` is therefore **not causally specific to the repair content**; it is a pure exact-grammar gate on (heading, four box labels, mark characters, optional evidence-line shape, pointer existence, trailing-bytes).

**Why this does not kill C1 (tradeoff, not defect):**
1. Kill-rule limb enumeration is exclusive: (a) `canonical=0` at final measured revision — false (HEAD reads clean); (b) a tested hidden/commented/duplicate checklist passes — false (Section 3, 6/6 caught); (c) archive bytes lost — false (Section 5); (d) post-scoring checker amendment — false (checker hash frozen since `3546f70`). A marker-only pass is not a listed limb.
2. The claim's own `mechanical_limits` disclose the boundary: "Specific author-side grammar: x marks are rejected… Evidence pointer existence is checked, not semantic truth." An all-`[ ]` file with no evidence lines is within that grammar; the checker never asserted content semantics.
3. The predicate ("SHONEN.md conforms to the canonical four-box author-assessment grammar **with existing local evidence pointers**") describes the realized after-state — HEAD's boxes carry pointers to `SKILL.md`, `LOG.md`, `corpus/lessons/round-47-verifier-spotcheck.md`, `PROVINCE.md`, all of which exist — not a universal statement about every input the grammar admits.

**Smallest safe correction:** documentation only — record in the round-48 closure notes that the frozen counter is an exact-grammar gate and that do-nothing marker files pass it, so later rounds do not misread `canonical=1` as evidence of assessment substance (mirrors the R2 lesson: frozen plain targets should be anchored so prose cannot meet the target; here the grammar is already anchored, and the residual unchecked-box hole is the disclosed remainder). Do **not** amend the frozen checker to close this: the kill rule's fourth limb bars post-scoring amendment from validating this claim, and any hardened grammar (e.g. evidence line mandatory per box, or ≥1 `[~]` pointer required) can only apply to future claims.

**Second causality caveat — tree-composition dependence of the after-result.** The literal `counter_cmd` is `--root {tree}` with `{tree}` unspecified; the after-verdict depends on the tree exporting the pointer targets:

```text
H1 SHONEN.md alone in tree:                        canonical=0 finding=SF-POINTER exit=1
H2 all targets except box-3 lessons pointer:       canonical=0 finding=SF-POINTER exit=1
H3 full 5-file measure.py composition:             canonical=1 finding=SF-CLEAN  exit=0
```

A verifier exporting only SHONEN.md would see exit=1 and could wrongly record a claim failure. The lane's `measure.py` already implements the correct composition (H3 reproduces the after-line). Correction: for future claims, name the exported file set inside `counter_cmd` documentation; no change to this frozen claim's measurement, which used the 5-file composition.

## Section 3 — kill-rule limb 2 attack matrix: hidden / commented / duplicate checklists

All variants are **caught**; none passes the frozen checker. `canon` = exact canonical form used as carrier.

```text
dup-full-second-checklist   canon + canon                          → canonical=0 SF-TRAILING
dup-html-comment            canon + <!-- canon -->                 → canonical=0 SF-TRAILING
commented-history           canon + <!-- - [~] old box -->         → canonical=0 SF-TRAILING
hash-comment-lines          canon + "# historical note"            → canonical=0 SF-TRAILING
extra-prose                 canon + blank + prose paragraph        → canonical=0 SF-TRAILING
leading-blockquote          blockquote interleaved between boxes   → canonical=0 SF-BOX
fifth-box                   canon + 5th box                        → canonical=0 SF-TRAILING
wrong-order                 boxes 1/2 swapped                      → canonical=0 SF-BOX
x-mark-evidence             all [x] with evidence                  → canonical=0 SF-VERIFIER
x-mark-no-evidence          all [x], no evidence lines             → canonical=0 SF-EVIDENCE
bom                         UTF-8 BOM + canon                      → canonical=0 SF-PREAMBLE
heading-typo                em-dash → hyphen in heading            → canonical=0 SF-PREAMBLE
crlf                        CRLF line endings                      → canonical=0 SF-NEWLINE
no-trailing-newline         final newline stripped                 → canonical=0 SF-NEWLINE
```

(Fixture note: the lane's pre-freeze `commented` fixture reported SF-PREAMBLE because its comment preceded the preamble; my `commented-history` places it after the canonical bytes and correctly lands SF-TRAILING. Finding code differs by placement; the catch is what matters, and both placements are caught.)

## Section 4 — evidence-pointer attacks

```text
ptr-nonexistent    Evidence: NOPE.md                        → canonical=0 SF-POINTER
ptr-absolute       Evidence: /etc/hostname                 → canonical=0 SF-POINTER
ptr-dotdot         Evidence: ../SHONEN.md                  → canonical=0 SF-POINTER
ptr-directory      Evidence: corpus (a directory)           → canonical=0 SF-POINTER
ptr-double-slash   Evidence: corpus//lessons/… (non-normal)  → canonical=0 SF-POINTER
ptr-unicode-zwsp   Evidence: LO​G.md (zero-width space)  → canonical=0 SF-POINTER
symlink-inside     Evidence: LINK.md → real.md inside root   → canonical=1 SF-CLEAN  (existence-only, disclosed)
symlink-escaping   Evidence: ESC.md → /etc/hostname         → canonical=0 SF-POINTER (confinement enforced)
```

The two symlink results bound the pointer check exactly as disclosed: post-resolution existence inside the tree root is accepted (existence, not semantic truth), escape from the root is rejected.

## Section 5 — archive, provenance, identity (kill-rule limbs 1/3)

- **Archive retained:** base `903d47e:SHONEN.md` sha256 = `596122c0…` = kill-rule archive hash; `controls/shonen-before.txt` byte-equal to it; the drifted bytes persist in git history at base and in the committed control snapshot. Restoration replaced only the live file (`596122c0… → b1352168…` between base and HEAD; diff `903d47e..HEAD` touches SHONEN.md, QUALITY.md, SOURCES.md, the checker, round-48 lesson — no silent restoration-byte loss).
- **52 author marks** confirmed at base (`grep -c '^- \['` on `git show 903d47e:SHONEN.md` = 52), matching the claim's `before`.
- **Duplicate authority:** the only live "Promotion checklist" headings outside `SHONEN.md` are the checker's own expected-lines constant, historical round-25/31/33 report artifacts, and round-48 controls/reports. The counter reads only `root/SHONEN.md` — no second live checklist competes as authority.
- **Identity/provenance nuance (causality, not defect):** the landed after-bytes `b1352168…` are **not** the frozen control bytes `canonical-candidate.txt`. The landed form upgraded per-box evidence pointers (`SKILL.md`, `LOG.md`, `corpus/lessons/round-47-verifier-spotcheck.md`, `PROVINCE.md`) and set box 2 to `[ ]` (no end-to-end task claimed — consistent with the round-47 closure's honest-stop), where the freeze-time candidate used all-`[~]` with all-`LOG.md` pointers. Both forms satisfy the exact grammar and existing-pointer rule; the claim's `after` is a form verdict and holds for the realized bytes. Recorded so the closure notes attribute the after-state to the landed repair commit `3d7e042`, not to the freeze-time candidate text.

## Impacted axes

- **depth:verifiability** — C1 claim **stands**: both expectations reproduce under the frozen counter; every kill-rule attack available from local evidence is defeated; the marker-only counterexample is a disclosed mechanical-limit boundary, not a kill trigger. Two documentation-level corrections recommended to the integrator (marker-pass boundary note; name the 5-file tree composition for future `counter_cmd` docs). No checker amendment is safe or needed for this frozen claim.

## Reproducibility and cleanup

- Driver + receipts: scratch `/fast/scratch/hyaku/kasegi-r48/R48Review09/` (`battery.py`, `receipts.txt`, `checker-frozen.py`, per-case trees, `measure.py` work dir). All findings above are stated with exact commands and verbatim outputs; receipts were saved into this report and the scratch directory was removed after the report was written (named scratch fixtures only, per seat spec).
- Production tree, fleet, siblings, domain trees, git/jj state: untouched (read-only `git show/log/diff/ls-files` only). No delegation, no background jobs.
