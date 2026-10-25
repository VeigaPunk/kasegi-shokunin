# ImmutableSources — critic report (round 23, read-only)

**Seat:** KasegiR23.ImmutableSources-5 · **Role:** critic · **Axes judged:** depth:verifiability, coverage

## Verdict

The attacked framing — "the S006 correction requires a superseding new SOURCES row, not an edit to old source fields" — is **falsified as applied to S006**. Contract v1 rule 2's supersession mechanism is real and correct *for row-field defects*, but the r22 S006 defect is not a row-field defect. No registry row is warranted; the correct repair is a lesson erratum, not an S0NN supersession.

## Evidence (all local, re-opened this round)

1. **The defect is the lesson Gate cell, not the registry row.** Verifier M5 (`/home/vgpnk/Projects/shokunin/.ufo/waves/kaika-w3/kasegi-review.md:102,117,169`): "the Gate names the wrong section (M5): the sentence sits in 'How to Enable Safe Harbors (Program Owners & Admins)', not 'What is safe harbor?' … Entry is correct; registry record is not." The wrong string is `corpus/lessons/round-22.md:82`, the Gate-table `location` cell for S006.
2. **S006's immutable row fields are already true.** `corpus/SOURCES.md:12` anchor reads "What is safe harbor? and How to Enable Safe Harbors; current guidance says aligned as of 2026-01-01" — the correct heading is present (the row's anchor covers two sections because two quotes were taken; row order is cosmetic, not false). `scope` and `teaches` are accurate. The knowledge entry attributes the quote correctly: `corpus/knowledge/authorization-safe-harbor-and-scope.md:2` (source header) and `:20` ("S006, 'How to Enable Safe Harbors (Program Owners & Admins)': 'Adopting a Safe Harbor does not change the program scopes.'").
3. **Contract v1 rule 2** (`/home/vgpnk/Projects/shokunin/CORPUS.md:97-99`): "Only `status`, `recheck` and `used-by` change in place… A correction is a new row whose `teaches` opens `supersedes S0NN —`." The clause governs *registry row* corrections. It cannot fire here: there is nothing false in the row to correct.
4. **Record errata have their own mechanism.** `corpus/QUALITY.md:51` (draft R9): corrections append to historical lessons rather than rewriting filed assertions; fleet rule (`CORPUS.md:56`): "Corrections are new entries, never rewrites." The Gate table is part of the filed r22 lesson — append-only under the same discipline that produced M5's discovery.

## Falsifier (the strongest counterexample)

**Test:** quote-location cells live in three places — Gate table `round-22.md:82`, registry anchor `SOURCES.md:12`, entry header `authorization-safe-harbor-and-scope.md:2`. Only the first is wrong. If the "supersede the row" rule were applied here, the round would mint a new row (e.g. S028 `supersedes S006 —`) whose only delta is heading order in the anchor cell. That produces: (a) **duplicate authority** — two live rows claiming the same URL/scope, no `status` value in the contract enum (`queued|mined|rejected`, CORPUS.md census) expresses "superseded", so S006 stays `mined` and the census's mined-used-by check still resolves it; (b) **false provenance** — `opened: 2026-10-19` on a row written 2026-10-20 violates rule 1 ("write it only after opening the source in the round that writes the row"); a re-open for a cosmetic reorder is manufactured work; (c) **status/used-by churn** — the entry's `source: S006` and `corpus/README.md:39,197` references would dangle or need rule-2 logged flips, all to fix a line that lives in a different file.

The rule fails its own grounding: M5 is cited in `corpus/QUALITY.md:50` (draft R8) as evidence for registry immutability, but M5's exact located defect is a *record* defect already covered by R9 (`QUALITY.md:51`). R8 as drafted conflates two correction surfaces.

## Smallest warranted correction

1. **Round-23 lesson erratum** (no registry row): "`round-22.md:82` Gate location for S006 read 'What is safe harbor?'; observed correct location is 'How to Enable Safe Harbors (Program Owners & Admins)' — verifier `kaika-w3/kasegi-review.md:169`; registry anchor `SOURCES.md:12` and entry `authorization-safe-harbor-and-scope.md:2,20` already name the correct section. Filed cell left verbatim per append-only discipline."
2. **Narrow draft R8** (`corpus/QUALITY.md:50`): change "a corrected anchor or broadened scope is a new row" to "**a corrected anchor or scope *in a registry row*** is a new row beginning `supersedes S0NN —`; quote-location errors in filed *records* (Gate tables, lessons, logs) are R9 append-only errata and mint no row." Add: "a row is superseded only when one of its immutable cells is false; imprecision or reordering alone is not a defect."
3. **No change** to `SOURCES.md:12`, `authorization-safe-harbor-and-scope.md`, `corpus/README.md`, or `round-22.md:82`.

## Where supersession IS correct this round (kept)

`opened-source-snapshots.json` shows S029 (EUR-Lex CRA) and S030 (CNA Rules v4.2.0) snapshots opened 2026-10-20 — S022's anchor pins v4.1.0 and S024's scope carries a "not yet verified" caveat. Those are genuine row-field corrections (new version, broadened verified scope): contract rule 2 supersession is the right mechanism and the C2 claim's F07/F08 admission depends on it. Distinguishing "supersede when the row is wrong" (S022/S024) from "errata when the record is wrong" (S006) is exactly the boundary R8 must state.

## Scope limits

- I did not re-open the HackerOne URL; the heading claim is the verifier's recorded observation plus SafeHarborLocation's pending independent open. If that scout finds the entry's own attribution also wrong, the falsifier above flips and S006 *does* need a superseding row — the two-layer rule still holds, only the case classification changes.
- Read-only seat: no production edits; this report is the only write. No mid-flight checks run.
- Census commands were inspected, not executed against a hypothetical S028 row; the duplicate-authority consequence is derived from the frozen enum and `used-by` check in `CORPUS.md:135-150` [INFERENCE: behavior of a row that does not yet exist, grounded in the contract text].

Report: `.ufo/waves/round-23/build/ImmutableSources.md`
