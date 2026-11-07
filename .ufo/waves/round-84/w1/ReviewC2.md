# ReviewC2 — F60 `corpus/knowledge/osv-gcs-data-dump-layout.md` vs S118, QUALITY, PROVINCE, F59 (2026-11-06)

Reviewed against the pinned capture `corpus/source-snapshots/round-84/S118.txt`
(sha256 `e824a735…` verified), its manifest, QUALITY Q1-Q10/R-rows, PROVINCE.md, F59
(`osv-faq-post-import-record-lifecycle.md`) and SOURCES.md:130. Receipts:
`ReviewC2-receipts/ReviewC2-verification.txt` (my runs) and
`ReviewC2-receipts/c2-prefreeze-r84.txt` (cited control, copied).

**Verified clean (mechanical):** all six quotes verbatim at their anchors, occurrences=1,
word counts 17/8/13/7/15/12 equal the gate table; sha256/129 lines/5820 bytes match manifest
and registry row; every cited range lands on the intended text (:1 title, :2-17 nav incl.
record-quality page at 14, :31-60, :61-65, :66-96, :97-98, :102, :104, :109-119, :112, :114,
:121, :122, :123, :124-126); every "after/before the pinned span" statement true; the entry's
`recheck:` runs exit 0 and reproduces the control receipt byte-for-byte; entry gate (r83
bytes, sha256 `42f4b2ac…`, unchanged vs base a089ff3d, clean worktree) →
`ENTRY-GATE-RESULT pass` (spans=7 = six claims + the title span); `source-recheck.py
--selftest` 10/10 fail-closed; literal sweep independently rerun: 0 files for each quote over
the other 97 entries (98 total, "97" arithmetic correct); F59/F58/F57/F51 pointer files exist
and their descriptions here are accurate; S118 registry row: 11 cells, tier A, `queued`,
scope/teaches true. No tool installs (operator authorization unused).

**Verdict: no Major defect. Two Medium, one Low — exact replacement text below; the L1
applies.**

## M1 (Medium) — Claim 5's falsifiable rule asserts "finds nothing", which its quote does not support and the entry's own Limits disclaim

Q05 (S118.txt:121) says the dump "will always contain an ecosystem directory without the
`:.*` suffix" — it does not say suffixed directories are absent. The Limits section itself
concedes it is unknown "whether stale suffixed directories are deleted or only left
unrefreshed" (S118.txt:123 says only that exporting stopped). So the rule's consequence
"finds nothing" is neither derivable from the pinned span nor consistent with the Limits
bullet two paragraphs later. Replacement (passes G5: ≥8 words, cites `S118.txt:<n>`, not
drawn from source):

- Old: `Falsifiable rule: a script that looks for a dump directory named after a release-suffixed ecosystem string such as an Alpine version finds nothing, since the page exports those advisories under the base name without the suffix (S118.txt:121). A reader checks it by reading the first paragraph under "Ecosystem naming".`
- New: `Falsifiable rule: a script that resolves a release-suffixed ecosystem string such as an Alpine version to a dump directory of the same spelling is resolving a name the page does not export under: the advisories are exported under the base name without the suffix (S118.txt:121), and exports for the suffixed names have stopped (S118.txt:123). A reader checks it by reading the first paragraph under "Ecosystem naming" and the note at its end.`

## M2 (Medium) — Distinctness under-discloses the one real F59 overlap: the FAQ already states the per-ecosystem prefix omission inside F59 Claim 5's cited range

F59 Claim 5 cites S117.txt:94-100; line 99 reads "…contains a modified_id.csv file with the
same format, but only for vulnerabilities in that ecosystem and without the
`<ecosystem_dir>` prefix in the second column." — the same fact Claim 4 pins from
S118.txt:114. The bullet names only "the top-level modified_id.csv with its row format and
reverse-chronological order" as F59's csv ground, so "This entry pins different sentences …
the per-ecosystem prefix rule" reads as fresh ground when it is a re-pin (the literal sweep
stays 0 only because the sentences differ). The old wording also misdescribes F59: F59's
paraphrase attributes the reverse-chronological order to the per-ecosystem copy
(S117.txt:99-100), not the top-level file. Replacement (first Distinctness bullet; no new
G2 span syntax introduced):

- Old: `- F59 / S117 (`corpus/knowledge/osv-faq-post-import-record-lifecycle.md`) holds the FAQ's post-import statements, including that withdrawn records stay in the GCS exports with the withdrawn field (its Claim 2 paraphrase of S117.txt:117-118) and the top-level modified_id.csv with its row format and reverse-chronological order (its Claim 5). This entry pins different sentences from a different page: the full zip's withdrawn inclusion, the per-record path, the [EMPTY]/ directory, the per-ecosystem prefix rule and the ecosystem-naming rules. It does not restate the top-level format or the sort order.`
- New: `- F59 / S117 (`corpus/knowledge/osv-faq-post-import-record-lifecycle.md`) holds the FAQ's post-import statements, including that withdrawn records stay in the GCS exports with the withdrawn field (its Claim 2 paraphrase of S117.txt:117-118) and the modified_id.csv listing (its Claim 5, whose cited range S117.txt:94-100 also carries the FAQ's own statement that each per-ecosystem copy keeps the row format without the `<ecosystem_dir>` prefix in the second column — the same fact Claim 4 pins here from S118.txt:114). This entry pins the Data sources page's sentences: the full zip's withdrawn inclusion, the per-record path, the [EMPTY]/ directory, the per-ecosystem prefix rule and the ecosystem-naming rules. It claims nothing about the top-level format or the sort order beyond Claim 4's context paraphrase of S118.txt:114.`

With the registry row no edit needed: the row's "not the top-level modified_id.csv format and
order (S117 F59)" stays true of the entry's claims once the carve-out reads "beyond Claim 4's
context paraphrase".

## L1 (Low) — Not-claimed bullet lacks the in-house paraphrase carve-out Claim 4's context requires

Claim 4's support sentence states the top-level row format (`S118.txt:114, before the pinned
span`), but the Not-claimed bullet lists "row format" as simply not claimed, and the
Distinctness bullet said "does not restate the top-level format" — both contradicted in-house
unless the paraphrase is carved out (house style: F59 "…beyond Claim 5's paraphrase"; this
entry's own "the per-ecosystem zip beyond Claim 2's paraphrase"). Replacement:

- Old: `the top-level modified_id.csv location, row format and reverse-chronological streaming advice (S118.txt:109-119; F59 holds the FAQ statement of the same file);`
- New: `the top-level modified_id.csv location and reverse-chronological streaming advice, and its row format beyond Claim 4's context paraphrase of S118.txt:114 (S118.txt:109-119; F59 holds the FAQ statement of the same file);`

## Residual risk and verification gaps

- Offline review against the pinned capture by design: I did not fetch the live URL or list
  any gs:// object; capture authenticity rests on the manifest/R20-R21 provenance (url,
  fetched_utc, sha), which I checked for internal consistency, not against a fresh fetch.
- The entry gate's G5 checks rule shape (≥8 words, a `S118.txt:<n>` cite, not drawn from
  source), not truth; rule soundness is covered only by this review's content read.
- Claim 6's rule (stale suffixed dirs miss post-stop changes) and M1's replacement remain
  inferences from page statements; both are falsifiable only against the dump itself, which
  neither the entry nor this review accessed.
- Both M-fixes change rule/bullet text only; the six pins, anchors, claims count and the
  gate's spans=7 are untouched, so the r83 entry gate need not change.
