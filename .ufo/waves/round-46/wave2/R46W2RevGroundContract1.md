VERDICT: BROKEN

# R46W2RevGroundContract1: side-by-side review of re-ground rows of claim-package-contract.md

Scope: `corpus/knowledge/claim-package-contract.md`, section `## Re-ground (round 46)`. The seat spec names G1-G7; the committed section has G1-G21 and the intro (line 73) says "exactly rows G1-G21", so all 21 were checked. Tree: export of 5437afe (`git archive 5437afe | tar -x`), compared with the lane working tree: `cmp` equal for the entry, `claim-package-check.py`, and the exemplar `manifest.json`, `provenance.json`, `report.md`. `git diff --name-only 5437afe HEAD -- corpus` prints nothing (lane HEAD 0d121a2 only adds `.ufo/waves/round-46/wave2*` files). Base: `git cat-file -e 914ca0b...:<anchor>` succeeds for every anchor file, so no anchor was planted. The contract's diff against base is 30 insertions and 1 deletion.

## Findings (by severity)

### 1. G18 is OVERREACH: the row says "heading"; the gate does not check a heading
- Row: `report.md carries a "Scope excerpt" heading (case-insensitive); the gate does not check the excerpt's composition`. Anchor `claim-package-check.py:634-635`.
- Committed bytes: `sed -n '120p' corpus/instruments/claim-package-check.py` prints `SCOPE_EXCERPT = re.compile(r'scope\s+excerpt', re.IGNORECASE)`; line 634 is `    if not SCOPE_EXCERPT.search(text):`. `search` matches anywhere in the file, not a heading.
- Entry l.11 says only `"Scope excerpt" = verbatim policy text + URL + observed_at + content sha256`; it never says heading.
- Attacked with a one-delta mutant (`mut.py`, mutant G18): the `## Scope excerpt` heading renamed to `## Scope notes`, and the phrase "the scope excerpt is quoted elsewhere in this file." added as prose. Gate output: `RULE R-REPORT verdict=pass detail=scope-excerpt=ok,marker=ok,url=ok,cited=4,unbound=0`. The heading-only removal (G18b, no phrase anywhere) reads `RULE R-REPORT verdict=fail detail=scope-excerpt=absent`. So the check is "the text occurs", and the row claims a stronger check.
- Fix: reword the claim cell to `report.md contains the text "Scope excerpt" (case-insensitive) anywhere in the file; the gate does not check that it is a heading or the excerpt's composition`. Anchor 634-635 stays.

### 2. G19, G20, G21 are CIRCULAR (attribution): the rows cite entry lines for a fixture fact the entry never states
- Rows: G19 "Entry l.13 (conforming instance): the exemplar manifest carries schema_version"; G20 "Entry l.15 (conforming instance): ... external_effects_performed set to an empty list"; G21 "Entry l.11 (conforming instance): the exemplar report carries the literal marker".
- `grep -n exemplar corpus/knowledge/claim-package-contract.md` prints only lines 73, 95, 96, 97 (the re-ground section itself). Lines 7-16 never mention an exemplar.
- The fixture bytes do contain the strings: `exemplar/evidence/manifest.json:2` = `"schema_version": "evidence-manifest/v1",`; `exemplar/provenance.json:88` = `"external_effects_performed": [],`; `exemplar/report.md:88` = `No submission performed.` So the literal claims are true, but the row's only evidence is the subject it is about. It can witness nothing about l.11/l.13/l.15, and the "Entry l.N" label is not a claim the entry makes.
- Fix: cut G19-G21 from the table (or move them to a fixture note with no "Entry l.N" attribution). Cutting leaves 18 rows; `r46-c1-gate.py` `MIN_ROWS = 6` (line 58), so the counter's floor holds. Update line 73 ("exactly rows G1-G21") and the errata's `rows=21` expectation to match. This is for L1 to apply.

### 3. Silent omission (coverage): entry claims neither re-grounded nor declared historical
Line 73 says the current claims are exactly G1-G21, and its "Left historical" sentence lists only: the round-13 boundary note (lines 18-27), the DONE/APPROVED/claimable census (29-54), the validation command (56-62), and `OPERATOR-GATED` (line 12). The following l.7-16 claims are gate-enforced and in neither list:
- l.7 "lives at `claims/<program>/<slug>/`" (no check of the path shape in the gate)
- l.11 "program + official URL" (`HTTPS_URL` check, `claim-package-check.py:638-639`)
- l.13 "Artifact paths ... must stay inside the package, no symlink traversal" (`inspect_path`, 336-339)
- l.13 "`redactions:[]` is never claim-ready" (R-REDACT, 359-427)
- l.14 "Non-empty decision chain" (`chain=empty`, 440-443)
- l.15 "commands + exit codes", "secrets attestation" (R-PROVENANCE, 502-538)
- l.16 "`claim_review` holds `hard_gates` + `subchecks` + `reviewer` ... fallback flag" (R-STATUS, 590-606)
Fix: either add rows for them or add them by name to the "Left historical and not re-grounded" sentence on line 73 with the reason. Silence is the defect.

### 4. Locator notes (faithful; verdict not affected)
- G1: claim is faithful; anchor 101-108 is the tuple only. Enforcement is `rule_files` `claim-package-check.py:279-281` (`for rel in SIX_FILES:`) and 295-296. Mutant G1 (`status.json` removed) reads `RULE R-FILES verdict=fail detail=missing=1,bad=0`. Its token spans lines; the counter matches it after whitespace normalisation (`r46-c1-gate.py:291`); I confirmed `normalised token in 101-108: True`. Consider widening the anchor to 279-281.
- G3: anchor 334 is the rejecting branch only; the positive branch is 332. Consider `332-334`.
- G8, G5, G6, G7: the anchors show the test that increments a counter; the raise is later (`:423-426`, `:473-476`). Outcomes verified by mutants (G8 `grant-miss=1`, G5 `identity=1`, G6 `digest-mismatch=1`, G7 `signal-bad=1`).
- G13: "must be 64-hex" is the gate's rule (`:525`); entry l.15 names the field only. Faithful to bytes; attribution wording.
- G11: "per transition" is per-agent field presence (`:497`); the gate does not check coverage against `provenance.transitions`. Undisclosed limitation; a reword ("each agent entry carries ...") would make it exact.

### 5. Rows that are faithful and disclose their narrowing (confirmed)
- G12 narrow, disclosed: presence only. Mutant pin deleted → `RULE R-PROVENANCE verdict=fail detail=pin=absent`; commit `zz` → `detail=pin=commit`. Remote/commit checks at `:518-523` are real.
- G16 narrow, disclosed: "checks it only against the manifest's producer and verifier names". Case variant of producer (`EXEC-EXEMPLAR-PACKAGE`, G16) → `detail=reviewer=not-distinct`. Identity `exemplar-custodian` (named in no receipt, G16b) → `RULE R-STATUS verdict=pass detail=manifest=bound,reviewer=distinct,gates=6/6,claimable=false,blocker=named`. The narrowing is real and as disclosed.

### Rows checked faithful (claim is an entry claim; anchor says it; mutant flips exactly that rule)
| row | entry line | anchor lines | class | evidence (mutant on exemplar copy; control = unmodified copy WELL-FORMED 8/8) |
| --- | --- | --- | --- | --- |
| G1 | l.7; table l.11-16 | :101-108 (+ use :279-281) | faithful | G1 → `R-FILES ... missing=1` |
| G2 | l.13 | :305 | faithful | schema `/v2` → `schema=evidence-manifest/v2` |
| G3 | l.13 | :332-334 | faithful | polarity `neutral` → `artifacts=4,polarity-bad=1` |
| G4 | l.13 | :354 | faithful | all negative → `artifacts=4,positive=0` |
| G5 | l.13 | :413-415 | faithful | verifier = producer upper → `receipts=4,identity=1` |
| G6 | l.13 | :407-409 | faithful | scanned digest `0`*64 → `artifacts=4,digest-mismatch=1` |
| G7 | l.14 | :460 | faithful | `scope_signal` OBJECTION → `chain=3,signal-bad=1` |
| G8 | l.14 | :457-458 | faithful | `matched_grant_id` "" → `chain=3,grant-miss=1` |
| G9 | l.14 | :467 | faithful | head `1`*64 → `chain=3,head=mismatch` |
| G10 | l.14 | :471 | faithful | expected head changed → `chain=3,head-manifest=mismatch` |
| G11 | l.15 | :497 | faithful (see note 4) | delete `resolved_model` → `agents=2,agents-bad=1` |
| G13 | l.15 | :524-525 | faithful (see note 4) | `policy_sha256` `abc` → `policy_sha256=bad` |
| G14 | l.15 | :527-528 | faithful | `["git push"]` → `external_effects_performed=not-empty` |
| G15 | l.16 | :585-588 | faithful | `sequence` changed → `manifest_sha256=mismatch` |
| G17 | l.11 | :636-637 | faithful | marker removed → `marker=absent` |

Counter (instrument of record, read-only, entry mode, run on the export root with scratch TMPDIR): `python3 -I corpus/instruments/r46-c1-gate.py --entry corpus/knowledge/claim-package-contract.md --root <export>` printed `row G1 ok=1 read=token-located` ... `row G21 ok=1 read=token-located` and `reground entry=claim-package-contract.md rows=21 ok=21 files=4 distinct=1 exit=0`. The counter sees 21/21 because it only locates tokens; all semantic findings above come from the reading.

## Do-nothing control and discrimination
- Control: unmodified copy of the exemplar: `package=.../ctrl/pkg rules=8 pass=8 fail=0 verdict=WELL-FORMED exit=0`. Gate selftest: `selftest cases=10 failures=0`.
- Each mutant flips only its cited rule (the others stay pass, aside from R-STATUS where manifest bytes change, which I did not read).
- Counter discrimination: control copy with `claim-package-check.py` line 334 blanked: `row G3 ok=0 read=token-not-in-lines` and `reground ... rows=21 ok=20 files=4 distinct=1 exit=1`.

## Limitations
- I ran the counter's entry mode on the exported tree, not the lane's recheck line in the lane. The bytes are equal (cmp, above), so the result should be identical; I did not run the lane line itself.
- Not checked: `claim-gates.md` re-ground rows (another seat), the aggregate L1-L7 gate, the F28 entry, the landing gate.
- Mutants were built from the exemplar with `json.dump(indent=1)`; this changes manifest bytes for G10/G15, which also trips R-STATUS. I read only the cited rule's line.
- `_identities` (`:548-560`) is read as the set of producer/verifier names in the manifest's redaction receipts; G16 confirms it.
- Semantic class labels are my judgment; the counter cannot grade them.
- This report is the one new untracked file in `.ufo/waves/round-46/wave2/`, written at the path the seat spec names. Nothing was committed, staged, or otherwise mutated in git; scratch was removed.
