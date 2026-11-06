# ReviewC2 — round-81 w1 — adversarial review of the C2 draft entry (S115, OSV GET /v1experimental/importfindings/{source})

Reviewed: `.ufo/waves/round-81/w1-input/osv-importfindings-record-quality-feedback.md` against `corpus/source-snapshots/round-81/S115.txt` (sha256 `e304eb88c7d79a6d2a1e4369c3e9a4fcf18f3ff4aabd6ad86466e85daf3f6f7f`, 44 lines, 2224 bytes — re-measured, matches), `corpus/source-snapshots/round-81/manifest.json`, and `corpus/QUALITY.md` Q1–Q10. Receipts: `ReviewC2-receipts/01…06`. No language server answers `.md`; all checks are text-level (`sed -n '<n>p'`, `grep -n`) against the committed bytes.

## Findings

### F-1 — HIGH — the Distinctness subject sweep is false the moment the entry lands (already false in this worktree)

The draft says:

> Subject sweep `grep -rli 'importfindings' corpus/knowledge/` (2026-11-06, before this entry) prints nothing and exits 1; `grep -rli 'source.yaml' corpus/knowledge/` and `grep -rli 'home database' corpus/knowledge/` likewise print nothing.

All three greps as written now print `corpus/knowledge/osv-importfindings-record-quality-feedback.md` and exit 0 (receipt 02): the landed copy is already on disk — untracked (`??`), byte-identical to the draft, listed in `corpus/instruments/knowledge-expected.txt:69`, with the S115 registry row and its used-by amendment staged in `corpus/SOURCES.md` (:127, :278). Every re-verifier who runs the entry's own sweep gets one hit and rc=0 — the entry fails the very check it cites as its distinctness evidence. Stale-on-landing verification line, the R16 stale-premise / Q1 fail-closed class.

**Replacement (paste over the whole bullet):**

```
- Subject sweep over every other entry, `grep -rli 'importfindings' corpus/knowledge/ | grep -vx corpus/knowledge/osv-importfindings-record-quality-feedback.md`, prints nothing and exits 1 (run 2026-11-06 with and without this entry present); `grep -rli 'source.yaml' corpus/knowledge/ | grep -vx corpus/knowledge/osv-importfindings-record-quality-feedback.md` and `grep -rli 'home database' corpus/knowledge/ | grep -vx corpus/knowledge/osv-importfindings-record-quality-feedback.md` likewise print nothing.
```

Verified land-stable (receipt 03): with the entry present the pipeline prints nothing and exits 1 for all three subjects; pre-landing, the first grep's empty output feeds `grep -vx`, which selects nothing and exits 1, so the sentence holds in both states — and any third file mentioning a subject still turns the sweep red.

### F-2 — LOW — Claim 4 paraphrase states an inference with a page cite that does not carry it

> The call takes one parameter, and that parameter is part of the URL, not a request body (S115.txt:36).

"Part of the URL" is carried by the template at S115.txt:37, not the cited :36; "not a request body" is an inference from the page's silence, stated as page fact under a :36 cite. No other paraphrase, falsifiable rule, or rejected over-generalization in the six claims overruns the page (each was checked against its line; the entry contains no literal `[INFERENCE]` markers).

**Replacement (the paraphrase sentence of Claim 4):**

```
The call takes one parameter, and the page gives that parameter to construct the URL (S115.txt:36), whose template carries it as the path segment (S115.txt:37); the page names no request body.
```

Both edits are outside quoted spans, so B8's G2/G4 bindings are unaffected.

## Checked clean (all receipts under `ReviewC2-receipts/`)

- **Quotes (Q3):** all six pinned quotes verbatim at S115.txt lines 25, 32, 34, 36, 37, 38; file-occurrences exactly 1 each; word counts 14/12/23/18/1/12 match the Gate table's `len(quote.split())` figures (receipt 01). Exactly 6 span patterns `"…" (S115.txt:<n>)` exist in the entry — the Gate table cells do not double-count.
- **Header (Q1/Q10):** lines 3/4/5 byte-clean (no CR, no trailing space, em-dash `—` after `source: S115`); recheck line parses under `bash -n`, is `cd`-prefixed, and is exactly the string B8's G1 requires.
- **Gate facts:** snapshot sha256/44 lines/2224 bytes and the 16418-byte raw page all match the manifest; `fetched_utc 2026-11-06T20:11:18Z`; `url` = `capture_url` = `http.final_url` at 200. Non-pinned cites verified: nav link "Properties of a High Quality OSV Record" at :14, case-sensitivity note at :39, request sample :41, response :43.
- **B8:** named run prints `ENTRY-GATE sid=S115 claims=6 want=6 spans=6 mislocated=0 overlong=0 claimless=0 unpinned=0 header=ok` / `ENTRY-GATE-RESULT pass`, rc=0; live `--selftest` ok; scratch probe moving one anchor (25→26) fails red (`mislocated=1`, rc=1) — the gate is not vacuous on the mislocation limb (receipt 05).
- **Recheck:** live run prints `S115:sha256 OK` plus six `S115:<pin> OK occurrences=1 anchor=<n>-ok` lines, rc=0; the committed receipt `.ufo/waves/round-81/controls/c2-prefreeze-r81.txt` matches the entry's Gate description line-for-line (receipt 06).
- **Distinctness path:line cites:** `osv-post-v1-query-contract.md:31` is a packed line whose tail carries the case-sensitivity rule quoting `(S108.txt:53)` — cite correct (the line head is the name rule; do not "fix" this cite); `:75` carries the Limits bullet listing "the experimental endpoints, S108.txt:5-9" — cite correct (receipt 04). Sibling files for F54/F55/F56/F31 all exist; registry rows S080/S108/S112/S113/S114/S115 present; S115 row URL identical to the manifest URL. The subject sweeps minus the entry itself (corrected form) confirm no other entry holds any of the six clauses.
- **Q5/Q4/Q6:** each claim has a falsifiable rule and a rejected over-generalization tied to its line; attribution stays the OSV project's page ("OSV.dev's quality bar", "home databases"); documentation-only — the only executable line touches local committed bytes.

## Residual risk

- Only B8's mislocation limb was adversarially probed here; header/claimless/unpinned limb mutation is MutEntryGate's seat.
- `S108.txt:53` was not re-opened (admitted F51 capture; the draft cites F51's entry line, which was verified).
- The corrected sweep is verified in the current tree state (entry present, untracked); its pre-landing behavior is analytic (empty input → `grep -vx` rc=1), not separately executed.

## Verification gaps

None blocking: every finding carries a reproducible receipt, and every entry claim exercised was confirmed.
