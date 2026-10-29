VERDICT: BROKEN

Scope: re-ground rows G9-G17 of `corpus/knowledge/claim-gates.md` (section `## Re-ground (round 46)`), checked against committed bytes at 5437afeaf9b642c267bba3c31f00ae701e49da68 (exported with `git archive` to a scratch tree; the lane `corpus/` equals it apart from untracked `__pycache__`). Entry file is byte-identical to the committed one (`git cat-file -p 5437afea:corpus/knowledge/claim-gates.md | diff - corpus/knowledge/claim-gates.md` printed nothing). Anchor file: `corpus/instruments/claim-package-check.py`.

Verdict basis: row G17 is `overreach`. Rows G9, G10, G11 are `faithful`. Rows G12, G13, G14, G15, G16 are `narrow`, of which G12 and G14/G15 need wording or anchor fixes. No row is `circular`.

## Table

| row | entry line | anchor lines | class | evidence |
|---|---|---|---|---|
| G9 | L36-37 | :469-472 (head_expected defined :435 = `manifest.get('expected_head_sha256')`) | faithful | Entry: "`head_sha256` = final decision's `decision_sha256` = `manifest.expected_head_sha256`". Mutant: manifest `expected_head_sha256` set to other digest → `RULE R-CUSTODIAN verdict=fail detail=chain=3,head-manifest=mismatch`. Control (unmodified exemplar) → `RULE R-CUSTODIAN verdict=pass detail=chain=3,grant-miss=0,signal-bad=0,head=bound`. |
| G10 | L36-37 | :465-467 | faithful | Mutant: `head_sha256` and manifest expected both set to `a`×64 (≠ final `decision_sha256` `46b50b…9bf9f`) → `RULE R-CUSTODIAN verdict=fail detail=chain=3,head=mismatch`. Gate's final decision is `chain[-1]` (:462), matching the entry's "final decision". |
| G11 | L69 | :584-589 | faithful | Mutant: one `\n` appended to `evidence/manifest.json` (status unchanged) → `RULE R-STATUS verdict=fail detail=manifest_sha256=mismatch`. Control passes. |
| G12 | L72-73 | :598-606 | narrow (role clause unmarked in row; listed in "Claims left historical" as "the `kx-reviewer` role") | Mutants: `fallback:"false"` (string) → `RULE R-STATUS verdict=fail detail=reviewer:fallback`; `requested_model:"  "` → `detail=reviewer:requested_model`; `role:"not-kx"` → `RULE R-STATUS verdict=pass detail=manifest=bound,reviewer=distinct,gates=6/6,claimable=false,blocker=named`. `grep -n "kx-reviewer\|'role'\|producer_identity\|'state'" claim-package-check.py` printed nothing (exit 1). Row omits `role` without saying so inline; the historical paragraph covers it, so acceptable with a reword (below). |
| G13 | L74 | :607-608 (`_identities` :548-560 reads only `redactions[].producer/verifier`) | narrow (row says so) | Mutant: `reviewer.identity = exec-exemplar-package` (a receipt producer) → `RULE R-STATUS verdict=fail detail=reviewer=not-distinct`. Mutant: `status.producer_identity = exemplar-reviewer` (= reviewer identity, not a receipt name) → `RULE R-STATUS verdict=pass …`. Confirms the row's "narrowed to: differs from every producer and verifier named in the redaction receipts" is accurate. |
| G14 | L75-76 | :594-597 (key presence, NOT in row's anchor cell) and :612-613 | narrow (row says so) | Exemplar as shipped (`no_duplicate_or_prior_submission: "PENDING"`, `claimable: false`) → `RULE R-STATUS verdict=pass …claimable=false,blocker=named`. Same with `claimable: true` → `RULE R-STATUS verdict=fail detail=claimable=true,gates-not-pass=1`. `authorization` key deleted, claimable false → `RULE R-STATUS verdict=fail detail=gates-missing=1`. Narrowing is accurate; the key-presence half cites :594-597, which the row's anchor omits. |
| G15 | L77 | :595 (presence) and :614 | narrow (row says so: "narrowed the same way as G14") | `operator_attribution: "FAIL"`, claimable false → `RULE R-STATUS verdict=pass`. Same with claimable true → `RULE R-STATUS verdict=fail detail=claimable=true,gates-not-pass=1`. Row's anchor omits :595; should add it. |
| G16 | L68 | :617-619 | narrow (row says so) | Mutant: claimable true, all hard gates PASS, `finding_count: 0` → `RULE R-STATUS verdict=fail detail=claimable=true,finding_count=bad`. Same with claimable false → `RULE R-STATUS verdict=pass …`. Narrowing accurate. |
| G17 | L48 | :138 and :140 (row cites :140 only) | **overreach** | See G17 detail below. |

## G17 detail (the BROKEN row)

Entry L48 (quoted): `` `/(api[_-]?key|secret|token|password|bearer)\s*[:=]\s*["']?[A-Za-z0-9_\-]{16,}/i` ``
Committed :140 (quoted): `('credential', re.compile(rb'(?i)\b(?:api[_-]?key|secret|token|password)\b\\?["\']?\s*[:=]\s*\\?["\']?[A-Za-z0-9_\-]{16,}')),`
Committed :138 (quoted): `('bearer', re.compile(rb'(?i)\bbearer\s+[A-Za-z0-9_.\-]{16,}')),`

Method: each string placed as `notes.txt` in a copy of the exemplar; gate run; entry L48 regex run through Python `re` with `re.I` on the same string. Output (verbatim):

```
control-short-token      entry-L48=False committed=pass   | RULE R-NOSECRET verdict=pass detail=files-scanned=ok,symlinks=0,oversize=0,hits=0
control-benign-prose     entry-L48=False committed=pass   | RULE R-NOSECRET verdict=pass detail=files-scanned=ok,symlinks=0,oversize=0,hits=0
s1-api_key-bare          entry-L48=True  committed=FLAG   | RULE R-NOSECRET verdict=fail detail=hits=1,first=notes.txt,shape=credential
s2-GITHUB_TOKEN-equals   entry-L48=True  committed=pass   | RULE R-NOSECRET verdict=pass detail=files-scanned=ok,symlinks=0,oversize=0,hits=0
s3-client_secret-colon   entry-L48=True  committed=pass   | RULE R-NOSECRET verdict=pass detail=files-scanned=ok,symlinks=0,oversize=0,hits=0
s4-DB_PASSWORD-quoted    entry-L48=True  committed=pass   | RULE R-NOSECRET verdict=pass detail=files-scanned=ok,symlinks=0,oversize=0,hits=0
s5-bearer-colon          entry-L48=True  committed=pass   | RULE R-NOSECRET verdict=pass detail=files-scanned=ok,symlinks=0,oversize=0,hits=0
s6-bearer-space          entry-L48=False committed=FLAG   | RULE R-NOSECRET verdict=fail detail=hits=1,first=notes.txt,shape=bearer
s7-token-spaced-equals   entry-L48=True  committed=FLAG   | RULE R-NOSECRET verdict=fail detail=hits=1,first=notes.txt,shape=credential
s8-api-dash-key-equals   entry-L48=True  committed=FLAG   | RULE R-NOSECRET verdict=fail detail=hits=1,first=notes.txt,shape=credential
```

What this shows:
1. Unmarked narrowing. The `\b` before the label (:140) means `GITHUB_TOKEN=`, `client_secret:`, `DB_PASSWORD="…"` (s2-s4) are not hits, while the entry's L48 flags them. The row names only the bearer alternative as narrowed; the word-boundary narrowing is not stated. The row's claim ("A labelled `api_key`, `secret`, `token` or `password` … is a secret hit") is therefore not what the committed bytes say.
2. Wrong description of the bearer alternative. The row says the bearer alternative "the gate checks in a separate pattern". The only separate pattern is :138, which matches `bearer` followed by whitespace and a token (s6 hits; s5 `bearer: …` does not). The entry's `bearer[:=]` form (s5) is not checked. The historical paragraph separately lists "the `bearer` labelled pattern as the entry writes it in one regex (L48)" as historical, so G17 contradicts the paragraph.
3. Anchor incomplete: the row cites :140 only; the claimed bearer check is at :138.
4. Counter blind spot: `r46-c1-gate.py --entry` reports `row G17 ok=1 read=token-located` (token `('credential', re.compile(rb'(?i)` is present at :140). The counter cannot see this; it is a semantic failure.

Discrimination: the controls (`token: short`, benign prose) are not hits in either regex, so the gate is not trivially flagging everything; the unmodified exemplar passes R-NOSECRET.

## Rows to cut or reword

- **G17 (required):** either cut the claim and move it to "Claims left historical", or reword to the committed behaviour: "A bare labelled `api_key`, `secret`, `token` or `password` (word-bounded label) followed by `:` or `=` and 16 or more token characters is a secret hit; narrowed: compound labels such as `GITHUB_TOKEN=` or `client_secret:` are not hits (committed `\b` at :140), and the entry's `bearer` followed by `:` or `=` is not checked (the committed bearer pattern at :138 is `bearer` + whitespace + token)." Add :138 to the anchor cell.
- **G12 (wording):** add "narrowed: the committed gate does not check `role === 'kx-reviewer'` (historical, see the paragraph below the table)".
- **G14 (anchor):** add :594-597 to the anchor cell (the "key presence only" half depends on it).
- **G15 (anchor):** add :595 to the anchor cell.

G9, G10, G11, G13, G16 need no change.

## Limitations

- The lost checker (`~/Projects/bounties/ops/claim-check.mjs`) is not present; "entry says" means the entry's own text. I did not run `anchorcheck.py` (restoration-only, fails closed by design).
- Semantic results are from single-field mutants on the exemplar fixture and the string set above; they are not exhaustive. Regex behaviour assessed with Python `re` on the committed bytes; the entry's regex was run with `re.I` as a stand-in for JS `/i`.
- Lane `corpus/` has untracked `__pycache__` and an untracked `corpus/instruments/r35-fixtures/D4/.ufo/...` file not in 5437afea; not used, not in G9-G17 scope.
- Not checked: F28, the landing gate, rows G1-G8 and G18-G25, and the other counter (C2).
- Scratch directory removed on exit; no git mutation, no commit, no edits outside this report.
