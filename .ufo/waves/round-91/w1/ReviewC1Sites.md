# ReviewC1Sites — C1 tranche 6: semantic review of the six landed rows (round 91)

Seat: ReviewC1Sites (reviewer/attack, leaf). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Freeze `53ab692a7b544c35141e2b19f7413cbdb767c1ad` → C1 landing `8a1a00c639ba808a701d1f186aac9ebd0045deaa`;
labels `e993fd181e320f1f21e06b05e16c68b0f07cff76`; map `.ufo/waves/round-91/c1/repair-map.tsv`.

Scope confirmed: the landing commit touches exactly one file, `corpus/knowledge/triage-thresholds.md`
(`git diff --numstat` = `6 6`), and the six edited lines are exactly the six map sites (141, 142, 226, 368,
454, 457). Nothing in the frozen `c1/ c2/ controls/ l1/` bytes was modified.

Method: opened every cited entry at the landing rev (`git show <rev>:<path>`, numbered), judged the whole row —
main statement and every gloss, M90-3 — and, for the four em-dash rows, searched the whole named entry *and* the
whole corpus scope the column draws on (`corpus/knowledge/` + `SKILL.md`, per the column's own definition at
`triage-thresholds.md:36-40`) for any range that states the row's value. Row verdicts are semantic reads; I did
not execute the meter or any counter, so nothing here re-scores a frozen predicate.

## Verdict per site

| site | landed change | verdict | evidence (entry @ 8a1a00c) |
|---|---|---|---|
| 141 | `MAX` (`--max`) row: corpus-tie cell `MATCHES: mission-control.md:13-14` → `—` | **CORRECT** | `mission-control.md:13-14` is a heading + blank; `max` occurs in that entry only at L17 (`active.size == --max`, a loop bound) and L55/56/159 (model ids `:max`). Corpus-wide `--max` occurs only at `mission-control.md:17`; no `default 5` anywhere. No range states the default, so `—` is the honest cell. |
| 142 | `STAGGER_S` (`--stagger`) row: corpus-tie cell `MATCHES: mission-control.md:13-14` → `—` | **CORRECT** | Zero occurrences of `stagger` / `20 s` / `20s` in `mission-control.md` (whole entry). Corpus-wide `stagger` appears only in triage's own rows (142, 147, 422 console-string). No tie exists. |
| 226 | `unreadable file` row: corpus-tie cell `MATCHES: claim-gates.md:29-36` → `—` | **CORRECT** | `claim-gates.md` contains neither `readJson` nor `unreadable` (whole entry). Its custodian section (entry L29-37 = source L74-93) states chain / per-decision signal / grant / digest / three-way head binding only; the `present but unreadable` precheck is not stated. Em dash replaces a false `MATCHES`. |
| 368 | six cost inputs, `number`, unbounded: corpus-tie cell `MATCHES: ev-model.md:21-23` → `—` | **CORRECT** | `ev-model.md` never says `unbounded`; L49-51 names the cost fields without type or bound; L22-23 pins only `p_*` to [0,1] and `as_of`. Corpus-wide `unbounded` occurs only in this row (plus unrelated intake/osv/round-23 prose). `source-tree-loss-2026-09-28.md:112` gives the schema span `:40-45` but not the type/bounds. Em dash correct. |
| 454 | location cell `ev-model.md:6-20`, `SKILL.md:494-506` → `corpus/knowledge/ev-model.md:13-25`, `SKILL.md:494-506` (second token untouched) | **WRONG (row level)** — edited token CORRECT | Edited token verified: `ev-model.md:13-19` is the formula block (`p_success`, `gross_value`, `total_cost`, `adjusted_ev`) and L24-25 is "Missing inputs print `UNKNOWN` … fail-closed reporting"; no gloss in the row contradicts them. **Second token is dead**: `SKILL.md:494-506` at the landing rev is park-disposition/autopsy prose (`RETRY_TRANSIENT` / `RETIRE_AUTH` / `docs/autopsies/<id>.md`), with no EV formula. The claim lives at `SKILL.md:828-832` (formula) and `846-848` (UNKNOWN fail-closed). `SKILL.md` is byte-identical between `e993fd18` and `8a1a00c` (`git diff --numstat` empty), so the label author saw the same stale token. |
| 457 | location cell `claim-package-contract.md:9-16, 28-38` → `corpus/knowledge/claim-package-contract.md:9-16` | **CORRECT** | L9 = `File / Binding rules` header, L10 = separator, L11-16 = exactly six rows (`report.md`, `claim_checklist.md`, `evidence/manifest.json`, `custodian-receipts.json`, `provenance.json`, `status.json`). Gloss "§9.8 marks the convention-only rows" resolves inside the citing file: `triage-thresholds.md:440` (§9.8) names `schema_version`, provenance `pin`/`policy_sha256`/`external_effects_performed`, `status.severity`/`status.reward` as contract-by-convention. Dropping `28-38` loses nothing the row asserts (that span is status.json observed semantics, L29-54 if ever needed). |

**Overall verdict: 5/6 rows CORRECT; 1 row WRONG at row level (454).** All six *edited* tokens are correct and
every edit is the edit its label names — but row 454 still carries an unrepaired location token that resolves to
unrelated text, so the landing leaves that row only half-verifiable. This is a routed defect, not a re-score: the
frozen M9/M10 predicate passes on it by construction (see below).

## Routed defects

**D1 (HIGH, in tranche scope) — row 454 second location is stale; label set judged only one token.**
`corpus/knowledge/triage-thresholds.md:454` now reads
`` | EV formula + UNKNOWN fail-closed | `corpus/knowledge/ev-model.md:13-25`, `SKILL.md:494-506` | MATCHES (…) | ``
and the second location does not state the claim. Proposed repair (candidate label, tranche 7):
`` `corpus/knowledge/ev-model.md:13-25`, `SKILL.md:828-848` `` (formula 828-832, UNKNOWN fail-closed 846-848;
widen to 855 if the exit-code clauses are wanted).
Re-runnable:
```
git show 8a1a00c639ba808a701d1f186aac9ebd0045deaa:SKILL.md | sed -n '494,506p'   # park-disposition/autopsy prose
git show 8a1a00c639ba808a701d1f186aac9ebd0045deaa:SKILL.md | sed -n '826,855p'   # the EV formula + UNKNOWN fail-closed
git diff --numstat e993fd181e320f1f21e06b05e16c68b0f07cff76 8a1a00c639ba808a701d1f186aac9ebd0045deaa -- SKILL.md  # empty
```
Why the frozen predicate cannot see it: M5 only bounds-checks the *new* anchor (`1 <= lo <= hi <= lines`,
`knowledge-meter.py:282`), M9 binds each map row to the edit its label names (`:286-293`), and M10 checks set
equality of labelled vs mapped sites (`:294-299`). No limb re-resolves a token the map did not touch, so a passing
meter coexists with the dead token.

**D2 (MEDIUM, same table, NOT tranche 6 — unchanged by the landing: base line == after line).** The same falsity
class the tranche removes survives in three adjacent rows of the §8 schema table:
- `:367` `p_*` "`number`, `minimum: 0`, `maximum: 1`" cites `ev-model.md:15-16`, which is
  `gross_value` / `total_cost`; the bound is stated at **`ev-model.md:22-23`** ("schema pins `p_*` to [0,1]").
- `:369` `deadline` "`format: date-time`" cites `ev-model.md:22-23`, which states `as_of` datetime only —
  `deadline` occurs in that entry only as a field name (L51). No supporting range → em dash.
- `:370` `duration_p90`, `submission_buffer` "`number`" cites `ev-model.md:22-23`; neither field's type is stated
  in the entry (names only, L50-51). No supporting range → em dash.
These were not label-named, so M10 correctly reports "complete" for the six; they are a candidate tranche 7, and
worth naming because the C1 axis is verifiability.

**D3 (MEDIUM, out of tranche — table-wide `SKILL.md` token drift).** At `8a1a00c`, other `SKILL.md` tokens in this
same file do not resolve to their subjects either, e.g. row 144 (`MAX_ATTEMPTS = 2`, also row 58) cites
`SKILL.md:117`, which is a `provenance.json:29` path fragment, and row 459 (`appendLedger` 3500 B cap /
`gitMutationBlocker`) cites `SKILL.md:146, 245-247`, which are a scope/retirement table row and autopsy-table rows.
Row 454's second token is one instance of this class, not a one-off. Verified with
`git show 8a1a00c639ba808a701d1f186aac9ebd0045deaa:SKILL.md | sed -n '117p;146p;245,247p'`.

## Qualifiers (not defects)

- **Q1 (LOW):** the `Corpus tie` legend at `triage-thresholds.md:37-40` defines only `MATCHES` and `SUPERSEDES`;
  the `—` cell the tranche now uses four more times is a by-usage convention the legend never names (pre-existing:
  ~10 rows already carried `—`). A reader cannot distinguish "no corroborating range" from "not assessed".
- **Q2 (informational):** the four em-dash edits assert "no corpus tie", not "the value is wrong". The rows'
  main statements stay unverifiable against the lost source tree (absent since 2026-09-28), exactly as before; the
  repair is honest in that it no longer claims corroboration it does not have.

## Label file vs repair map (row by row)

`round91-labels.tsv` @ `e993fd18` has exactly 6 rows; the map has exactly 6 rows; every map row's
`citing-file:line` and old cell are the label's site and cited key; every map `new` is the edit the label's fix
text names (programmatic join, all six `True`).

| site | label's cited key | label's fix (abridged) | map `new` | match |
|---|---|---|---|---|
| 141 | `mission-control.md:13-14` | "Replace MATCHES with — (… `--max` only a loop bound at L17, never default 5)" | `—` | yes |
| 142 | `mission-control.md:13-14` | "Replace with — (… STAGGER_S / 20 s not stated anywhere in the entry)" | `—` | yes |
| 226 | `claim-gates.md:29-36` | "Replace with — (… unreadable-file precheck not stated; readJson absent)" | `—` | yes |
| 368 | `ev-model.md:21-23` | "Replace with — (… L22-23 pin only p_*; cost type/bounds not stated)" | `—` | yes |
| 454 | `ev-model.md:6-20` | "Repoint the first token to 13-25: formula L13-19 plus UNKNOWN fail-closed L24-25" | `` `corpus/knowledge/ev-model.md:13-25` `` | yes |
| 457 | `claim-package-contract.md:9-16, 28-38` | "Replace with claim-package-contract.md:9-16 (six-file table…)" | `` `corpus/knowledge/claim-package-contract.md:9-16` `` | yes |

Each label's stated evidence was independently re-checked against the entries and holds: L17 is the only `--max`
in `mission-control.md`; the entry has no `stagger`; `claim-gates.md` L29-37 is chain/per-decision/head binding
only; `ev-model.md` L49-51 is a field-name list; `ev-model.md` L13-19 is the formula block and L24-25 the UNKNOWN
fail-closed bullet; `claim-package-contract.md` L28 is blank, L29 a heading, L31-34 the `state` facts, L35-38 a
partial `verdict` bullet. Two label fix cells spell their target without the `corpus/knowledge/` prefix; the map
supplies it, which is exactly the edit form M9 requires (`knowledge-meter.py:34-38`), so that is not a divergence.
Map sha256 = `55d50b661bcf79ad5a435c7d7bc86e3954e9910f7dabc480236224170c8c0a7a`, equal to the frozen
`--map-sha256`.

## Residual risk and verification gaps

1. I did not run the knowledge meter or the C2 counter (out of seat); all six verdicts are independent semantic
   reads at `8a1a00c`, so D1 does not imply a predicate failure — it is invisible to it (see D1).
2. Breadth of the em-dash check: `corpus/knowledge/*.md` + `SKILL.md` (the column's own scope) plus a bounded
   recursive `*.md` grep over the rest of `corpus/` (knowledge, lessons, practice, instruments docs). No
   additional tie for any of the four values. `corpus/source-snapshots/` was not grepped: it holds source bytes,
   not corpus claims.
3. Line-number drift means a citation can be "correct at the time written, dead at the landing rev". I judged at
   `8a1a00c` only, as instructed; D3 shows the drift is broader than the six sites and deserves its own label set.
4. `SKILL.md` tokens in this table carry no revision pin; any repair of D1/D3 should state the rev it resolves at
   or the drift returns.

## Files written

- `.ufo/waves/round-91/w1/ReviewC1Sites.md` (this report)
- `.ufo/waves/round-91/w1/ReviewC1Sites-receipts/site-evidence.txt`
  (sha256 `1e1efc8fd7c457a3d4519cf4ea113c0ac6f5f484b266ae3b39c1efa5919b43b1`) — per-site commands and outputs:
  landing scope, the six after-lines, entry greps for 141/142/226/368, `ev-model.md:13-25`,
  `SKILL.md:494-506` vs `826-855`, `claim-package-contract.md:9-16`, §9.8, the tie legend, and the adjacent rows.
- `.ufo/waves/round-91/w1/ReviewC1Sites-receipts/label-vs-map.txt`
  (`3b55a663b9866d52ab246190b56a9c85a3c2ad1ea1f63a1e3666ecf247c74647`) — map + labels sha256, both tables, the
  six-row programmatic join.
- `.ufo/waves/round-91/w1/ReviewC1Sites-receipts/c1-diff.txt`
  (`623b64a66c7350134f1dc1ef35d25cdec9f567e18bce7fcb1b887268e39c9c62`) — the 6-line freeze→landing diff.
- `.ufo/waves/round-91/w1/ReviewC1Sites-receipts/meter-limbs.txt`
  (`2904531318072351edcb91c8b900a7b4577ded7eb05813ee2303a69bea8f29ad`) — M5/M9/M10 docstring and implementation
  excerpt.
- `.ufo/waves/round-91/w1/ReviewC1Sites-receipts/round91-labels.tsv`
  (`4f3ad6633ce3b24b5ee44e24e8e5d25a77d1b638b0eca7961227cfe27fe65506`) — byte copy of the cited label file at
  `e993fd18`.

Credential hygiene: no planted or real credential value was written; fixtures were not needed (all evidence is
`git show`/grep output over corpus text). The report and every receipt were checked with the round-91
credential-shape class (AWS session-token, Google signature, Azure SAS `sig` parameter, CloudFront signed-cookie
and signature names, AKIA/ASIA key ids, private-key headers, token/secret assignments): no hit, so no literal
pattern is reproduced here.
Scratch `/fast/scratch/hyaku/kasegi-r91/ReviewC1Sites` deleted before yield. No tooling installed.
