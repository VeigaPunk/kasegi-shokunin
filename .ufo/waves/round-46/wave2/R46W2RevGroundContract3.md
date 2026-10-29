VERDICT: BROKEN

Scope: side-by-side verification of re-ground rows G15-G21 in `corpus/knowledge/claim-package-contract.md`, section `## Re-ground (round 46)`, against the committed tree 5437afeaf9b642c267bba3c31f00ae701e49da68 (exported to scratch; the six files consulted are byte-identical to the lane working tree, checked with `cmp -s`). Read-only; no edits, no commits.

## Row table

| row | entry line (quoted) | anchor lines | class | evidence |
| --- | --- | --- | --- | --- |
| G15 | l.16 `status.json` … "`manifest_sha256` binds status to manifest bytes." | `corpus/instruments/claim-package-check.py:585-588` | faithful | 585 `actual = hashlib.sha256(manifest_bytes).hexdigest()`; 588 `if recorded.lower() != actual:`. Mutation: manifest byte appended, status unchanged → `RULE R-STATUS verdict=fail detail=manifest_sha256=mismatch`, exit 1. Control (unmutated exemplar) → R-STATUS pass. |
| G16 | l.16 "`reviewer` (distinct identity, requested/resolved model, fallback flag)" | `claim-package-check.py:607` | narrow (row says so) | 607 `if identity.strip().casefold() in _identities(manifest):`; `_identities` (l.548-560) reads only `manifest['redactions'][*].producer/verifier`. Reviewer = manifest verifier → `RULE R-STATUS verdict=fail detail=reviewer=not-distinct`. Reviewer = `EXEC-EXEMPLAR-PACKAGE` (case) → same fail. Reviewer = provenance-only agent name `exec-provenance-only` (not in manifest) → `RULE R-STATUS verdict=pass`, package `WELL-FORMED exit=0`. Row's narrowing is accurate. |
| G17 | l.11 report.md "literal marker "No submission performed"" | `claim-package-check.py:636-637` | faithful (anchor gap) | 636-637 `if NO_SUBMISSION not in text:` / `raise _GateFail('marker=absent')`. The literal itself is defined at l.121 `NO_SUBMISSION = 'No submission performed'`, outside the cited range. Mutation "No submission was made." → `RULE R-REPORT verdict=fail detail=marker=absent`; lowercase "no submission performed." → same fail (exact, case-sensitive literal). |
| G18 | l.11 "\"Scope excerpt\" = verbatim policy text + URL + observed_at + content sha256" | `claim-package-check.py:634-635` | **overreach** (claim cell says "heading") | 634-635 `if not SCOPE_EXCERPT.search(text):`; the predicate is defined at l.120 `SCOPE_EXCERPT = re.compile(r'scope\s+excerpt', re.IGNORECASE)` — no `^`, no `#`, no line anchor, searched over the whole report. Mutation: `## Scope excerpt` heading replaced by prose "The scope excerpt is reproduced below." → `package=... verdict=WELL-FORMED exit=0` with `RULE R-REPORT verdict=pass detail=scope-excerpt=ok,marker=ok,url=ok,cited=4,unbound=0`. The phrase's removal → `RULE R-REPORT verdict=fail detail=scope-excerpt=absent`. The gate does not verify a heading. The "does not check composition" half of the row is correct: observed_at line stripped → R-REPORT pass, exit 0. |
| G19 | l.13 `schema_version: "evidence-manifest/v1"` (conforming instance) | `corpus/instruments/fixtures/claim-package/exemplar/evidence/manifest.json:2` | faithful (field); instance-level | `sed -n 2p` → ` "schema_version": "evidence-manifest/v1",`. Schema mutated to v2 → `RULE R-MANIFEST verdict=fail detail=schema=evidence-manifest/v2`. Whole-package control: `package=.../exemplar rules=8 pass=8 fail=0 verdict=WELL-FORMED exit=0`. Entry l.13 itself does not name the exemplar; the "conforming instance" tag is a fixture fact, supported by the whole-package run, not by the single cited field. |
| G20 | l.15 `external_effects_performed: []` | `.../exemplar/provenance.json:88` | faithful | `sed -n 88p` → ` "external_effects_performed": [],`. Mutated to `["x"]` → `RULE R-PROVENANCE verdict=fail detail=external_effects_performed=not-empty`, exit 1. |
| G21 | l.11 literal marker (conforming instance) | `.../exemplar/report.md:88` | faithful | `grep -n "No submission performed" .../report.md` → `88:No submission performed.`; the absent-marker mutation fails R-REPORT (row G17 control). |

Counter check (counter v1.1, `r46-c1-gate.py --entry corpus/knowledge/claim-package-contract.md`, run in the export): `row G15 ok=1 read=token-located` … `row G21 ok=1 read=token-located`, final `reground entry=claim-package-contract.md rows=21 ok=21 files=4 distinct=1 exit=0`. The counter passes G18 although G18 is an overreach: the counter tests token location, not semantics.

Anchor shift control: each row's token is found only at the cited line (e.g. `token_hits_in_range= [634]`) and `hits=[]` when the anchor window is shifted +200 lines.

## Findings

1. **G18 is overreach → BROKEN (cut or reword).** The claim cell says the gate checks that report.md "carries a 'Scope excerpt' heading". The committed predicate (l.120, l.634-635) matches the phrase anywhere in the text; the prose variant passes WELL-FORMED. Reword the cell to: "report.md contains the phrase `scope excerpt` (case-insensitive, anywhere in the text; no heading is required; the excerpt's composition is not checked)". The same overstatement is in the gate's own docstring (`claim-package-check.py:74-75` and `:629`, "carries the `Scope excerpt` heading"); the L1 should decide whether to correct the docstring or only the row, since the instrument is shared production and was not edited here.
2. **G17 anchor is incomplete (reword/extend, not a verdict driver).** The literal `No submission performed` is defined at `claim-package-check.py:121`; cite `121` alongside `636-637`.
3. **G18 anchor is incomplete.** The regex that defines the check is at `claim-package-check.py:120`; cite it alongside `634-635`.
4. **G16 narrowing is accurate; keep it.** Narrowing confirmed by the provenance-only-identity run (passes). Limitation: `_identities` returns an empty set when `redactions` is not a list, so the R-STATUS distinctness check passes vacuously in that case; the full gate still fails via R-REDACT (`redactions` non-empty), and I did not run that variant.
5. **G19-G21 keep as fixture facts.** Each field matches the exemplar bytes, and the field mutations are load-bearing. The "conforming instance" tag is supported by the whole-package run (`verdict=WELL-FORMED exit=0`), which the rows do not cite; citing it would make the tag checkable. The entry lines do not name the exemplar, so these rows are not entry claims in the strict sense.
6. **G15 and G20 are faithful with no required change.**

## Limitations

- Scope: rows G15-G21 only. Not checked: G1-G14, counter v1.1 errata, the F28 entry, the landing gate.
- Mutation tests ran on scratch copies of the exemplar from the 5437afe export, through `claim-package-check.py` (read-only). `--selftest` was not run.
- HEAD (0d121a2) differs from 5437afe only in wave-2 spec/dispatch files (none under `corpus/`), so the corpus bytes read here are the lane's current ones.
- The counter was run only as the token-location control, not as a semantic judgment.
- No live target was touched; all checks are documentation/instrument-only.
