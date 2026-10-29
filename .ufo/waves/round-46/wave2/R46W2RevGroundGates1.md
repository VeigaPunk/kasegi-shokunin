VERDICT: HOLDS

Scope: side-by-side check of re-ground rows G1-G8 in `corpus/knowledge/claim-gates.md` (section `## Re-ground (round 46)`, lines 128-160), against the committed bytes. Tree: export of 5437afeaf9b642c267bba3c31f00ae701e49da68. The lane HEAD (0d121a2) differs from 5437afe only by five wave-2 `.ufo` files; `git diff --quiet 5437afe -- corpus` exited 0, so the lane corpus is identical to the export. The lane `corpus/` equals the export.

## Classification table

Format: `row | entry line | anchor lines | class | evidence`

| row | entry line | anchor lines | class | evidence |
|---|---|---|---|---|
| G1 | entry L10-11 | `claim-package-check.py:101-108` (constant `SIX_FILES`); enforcement at `:275-285` and `:295-296` | faithful (anchor weak, see F1) | control C-G1 |
| G2 | entry L20 | `:307-309` | faithful | control C-G2 |
| G3 | entry L23 | `:332-335` | faithful | control C-G3 |
| G4 | entry L21-23 (sha256 clause on L23) | `:340-347` | faithful | control C-G4 |
| G5 | entry L24 | `:354-355` | faithful | control C-G5 |
| G6 | entry L25-26 | `:407-409` | faithful (receipt-presence sub-claim on L25 not restated, see F2) | control C-G6 |
| G7 | entry L26-27 | `:413-416` | faithful | control C-G7 |
| G8 | entry L32-33 | `:460-461` | faithful (HARD_STOP sub-claim on L33 is listed as historical at L160, so no finding) | control C-G8 |

No row is `overreach`, `circular`, or `narrow` without saying so. No row is marked `narrowed` in the table, and none needs to be: each committed check says what the restated claim says. G1 is stronger than the claim (it also requires non-empty files and JSON objects).

## Entry lines and anchor lines (quoted, `sed -n`, run in the lane)

Command: `sed -n '10,11p;20,20p;23,24p;25,27p;32,33p' corpus/knowledge/claim-gates.md`
```
Required: `report.md`, `claim_checklist.md`, `custodian-receipts.json`,
`provenance.json`, `status.json`, `evidence/manifest.json` (L22–24).
- `sequence` is a number; `expected_head_sha256` key present.
  escape check); sha256 matches; `polarity` ∈ {positive, negative}.
- ≥1 positive-polarity artifact.
- Every artifact needs a redaction receipt with `artifact_sha256 ===
  scanned_artifact_sha256 === a.sha256` AND nonempty distinct producer/verifier.
- Every receipt must bind a manifest artifact digest; producer ≠ verifier.
- Per decision: `scope_signal` exactly `NO_SCOPE_OBJECTION` (any other value
  errors; `HARD_STOP` gets its own message AND the exact-signal message —
```

Command: `sed -n '101,108p;307,309p;332,335p;340,347p;354,355p;407,409p;413,416p;460,461p' corpus/instruments/claim-package-check.py`
```
SIX_FILES = (
    'report.md',
    'claim_checklist.md',
    'evidence/manifest.json',
    'custodian-receipts.json',
    'provenance.json',
    'status.json',
)
    sequence = manifest.get('sequence')
    if isinstance(sequence, bool) or not isinstance(sequence, (int, float)):
        raise _GateFail('sequence=not-number')
        if artifact.get('polarity') == 'positive':
            positive += 1
        elif artifact.get('polarity') != 'negative':
            polarity_bad.append(rel)
        try:
            with open(target, 'rb') as handle:
                actual = hashlib.sha256(handle.read()).hexdigest()
        except OSError:
            escape.append(rel)
            continue
        if actual != recorded.lower():
            digest_bad.append(rel)
    if positive < 1:
        raise _GateFail('artifacts=%d,positive=0' % len(artifacts))
        if not (isinstance(first, str) and isinstance(second, str)
                and isinstance(recorded, str)
                and first.lower() == second.lower() == recorded.lower()):
        if (not isinstance(producer, str) or not producer.strip()
                or not isinstance(verifier, str) or not verifier.strip()
                or producer.strip().casefold() == verifier.strip().casefold()):
            identity_bad += 1
        if decision.get('scope_signal') != 'NO_SCOPE_OBJECTION':
            signal_bad += 1
```

Enforcement site of G1 (cited by no row): `sed -n '275,285p;295,296p' corpus/instruments/claim-package-check.py` prints `for rel in SIX_FILES:` at 279, `if error in ('missing', 'notdir', 'escape', 'symlink', 'absolute', 'dotdot'):` at 281, `if error or os.path.getsize(target) == 0:` at 284, and `if missing or bad:` / `raise _GateFail('missing=%d,bad=%d' % (len(missing), len(bad)))` at 295-296. The JSON loop at 286-294 also covers `custodian-receipts.json`.

## Controls (do-nothing discrimination)

Method: for each row I built a scratch copy of the gate with only the anchored predicate neutralised (`if False:`, `and True):`, `or False):`, `for rel in ():`, or the custodian token removed from `SIX_FILES`). Each copy is a one-line `str.replace` with an asserted single match. I then ran the original gate and the neutralised copy on a scratch copy of the exemplar package with one violation injected. The control passes exactly when the anchored line is load-bearing. The original fixtures under `corpus/instruments/fixtures/claim-package/` were not modified; every mutant is in the scratch dir.

Original gate on the exemplar (baseline): `RULE R-FILES verdict=pass detail=files=6,missing=0,bad=0` ... `package=.../exemplar rules=8 pass=8 fail=0 verdict=WELL-FORMED exit=0`.

Printed by the run (orig = original gate, ctl = neutralised gate):
```
[G1] orig : RULE R-FILES verdict=fail detail=missing=1,bad=0
[G1] ctl  : RULE R-FILES verdict=pass detail=files=6,missing=0,bad=0
[G1-token] orig : RULE R-FILES verdict=fail detail=missing=1,bad=0
[G1-token] ctl  : RULE R-FILES verdict=fail detail=missing=0,bad=1
[G2] orig : RULE R-MANIFEST verdict=fail detail=sequence=not-number
[G2] ctl  : RULE R-MANIFEST verdict=pass detail=artifacts=4,positive=3,digest-bad=0,escape=0
[G3] orig : RULE R-MANIFEST verdict=fail detail=artifacts=4,polarity-bad=1
[G3] ctl  : RULE R-MANIFEST verdict=pass detail=artifacts=4,positive=3,digest-bad=0,escape=0
[G4] orig : RULE R-MANIFEST verdict=fail detail=artifacts=4,digest-bad=1
[G4] ctl  : RULE R-MANIFEST verdict=pass detail=artifacts=4,positive=3,digest-bad=0,escape=0
[G5] orig : RULE R-MANIFEST verdict=fail detail=artifacts=4,positive=0
[G5] ctl  : RULE R-MANIFEST verdict=pass detail=artifacts=4,positive=0,digest-bad=0,escape=0
[G6] orig : RULE R-REDACT verdict=fail detail=artifacts=4,digest-mismatch=1
[G6] ctl  : RULE R-REDACT verdict=pass detail=artifacts=4,receipts=4,missing=0,digest-mismatch=0
[G7] orig : RULE R-REDACT verdict=fail detail=receipts=4,identity=1
[G7] ctl  : RULE R-REDACT verdict=pass detail=artifacts=4,receipts=4,missing=0,digest-mismatch=0
[G8] orig : RULE R-CUSTODIAN verdict=fail detail=chain=3,signal-bad=1
[G8] ctl  : RULE R-CUSTODIAN verdict=pass detail=chain=3,grant-miss=0,signal-bad=0,head=bound
```
Injected violations: C-G1 removed `claim_checklist.md`; C-G1-token removed `custodian-receipts.json`; C-G2 `sequence` set to the string `"1"`; C-G3 one artifact `polarity` set to `"maybe"`; C-G4 one byte appended to `evidence/disclosure-timeline.txt`; C-G5 all three positive artifacts set to `negative`; C-G6 `redactions[1].artifact_sha256` set to 64 zeros; C-G7 `redactions[0].verifier` set to its producer; C-G8 `chain[1].scope_signal` set to `HARD_STOP`.

Reading: every row except G1-token is load-bearing for its own predicate. For C-G1-token the custodian file is still caught, by the JSON loop (`:286-294`), so the token `'custodian-receipts.json',` at line 105 does not carry the G1 claim for that file (F1).

Counter run, for reference only (token presence, not semantics): `cd <export> && python3 corpus/instruments/r46-c1-gate.py --entry corpus/knowledge/claim-gates.md` printed `row G1 ok=1 read=token-located` ... `row G8 ok=1 read=token-located` and `reground entry=claim-gates.md rows=25 ok=25 files=3 distinct=1 exit=0`. The same line appears from the lane. The counter does not show that any row is load-bearing; the controls above do that for G1-G8.

## Findings

F1 (G1, reword/re-anchor, not BROKEN). The G1 row cites `:101-108`, a tuple constant. The enforcing loop is `:279` (`for rel in SIX_FILES:`) with the verdict at `:295-296`. The token `'custodian-receipts.json',` is not what enforces the claim for that file, because the JSON loop at `:286-294` also covers it (C-G1-token). Suggested fix: re-anchor G1 on `corpus/instruments/claim-package-check.py:279-285` with token `for rel in SIX_FILES:`. Claim-faithfulness is not affected.

F2 (G6, G2, G7, reword, not BROKEN). Some sub-claims on lines the rows cite are not restated by the row and are not in the "Claims left historical" paragraph (line 160). They are: receipt presence "Every artifact needs a redaction receipt" (entry L25; committed `missing` check at `claim-package-check.py:417-420`); "Every receipt must bind a manifest artifact digest" (entry L27; committed binding at `:387-403`); and `expected_head_sha256` key present (entry L20; committed HEX64 check at `:310-312`). The committed gate enforces all three, so this is an omission, not an overreach. Suggested fix: add rows for them, or name them in the line-160 historical list. Line 130's general "every other line is historical" does not clearly cover sub-claims on cited lines.

F3 (subject of the claim, wording only). `claim-package-check.py:4-8` says the gate is a round-43 re-implementation derived from `corpus/knowledge/claim-gates.md`, and that the lost `claim-check.mjs` "was documentation-only for this lane". So G1-G8 establish that the committed re-implementation enforces what the entry describes. They do not establish that the lost checker did. Line 130 names the re-implementation as the anchor, but the rows restate lost-tool wording ("Required:", "is a number") in the present tense. Suggested rewording: prefix the claim column with "the committed re-implementation enforces". I did not classify any row as `circular`, because the anchors are executable code whose predicates I exercised with the controls above, and not the entry's own text.

## Limitations

- I checked only G1-G8 of `claim-gates.md`. I did not check G9-G25, the `claim-package-contract.md` rows, the F28 entry, or the landing gate.
- Controls use my own scratch mutants of one exemplar package. They show that each anchored predicate is load-bearing for the injected violation. They do not prove the gate matches the lost tool.
- The `--selftest` mode of the gate was not run.
- The counter is token-presence only. Its `files=3 distinct=1` is a boolean (`distinct`), not a count, as its source at `r46-c1-gate.py:177-179` shows.
- No commit, push, index or git mutation. The lane tree was only read (`sed`, `git diff --quiet`, `git archive` into scratch). Scratch under `/fast/scratch/hyaku/kasegi-r46/R46W2RevGroundGates1/` was removed on exit.
