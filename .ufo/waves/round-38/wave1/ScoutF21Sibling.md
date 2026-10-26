# ScoutF21Sibling — F21 (OASIS CSAF v2.0 / VEX) sibling-overlap reconnaissance

Round 38, claim C2 (coverage), frontier F21 = OASIS CSAF v2.0 VEX profile (S055). Receipt only; no deliverable file. Read-only: no lane or source tree was written. Run 2026-10-26T18:36Z.

## Command

```
cd /home/vgpnk/Projects/shokunin
P='CSAF|Common Security Advisory Framework|\bVEX\b|product_status|known_not_affected'
for d in $(ls -d *-shokunin | grep -v '^kasegi'); do
  for t in corpus SKILL.md PROVINCE.md; do
    [ -e $d/$t ] && grep -rnIE --exclude-dir=.ufo --exclude-dir=.git "$P" $d/$t
  done
done
grep -rnIE "$P" /home/vgpnk/Projects/shokuknow/merge/*/
```

Scope check: `ls -d *-shokunin` = 21 repos; minus kasegi = 20 sibling lanes, all scanned. shokuknow/merge has 21 subdirs (one per lane incl. kasegi), all scanned.
Scratch dir ($S under /fast/scratch/hyaku/kasegi-r38/ScoutF21Sibling) removed before yield.

## Hit list (case-sensitive pattern as specified)

Siblings: 1 hit in 1 file.
- `kake-shokunin/corpus/knowledge/security-txt-publishing.md:63`: "New fields are IANA-registered, optional by definition, and unknown ones must be ignored (S078); securitytxt.org already lists one extension, `CSAF` (S079)."

shokuknow/merge/*/: 0 hits.

## Widened controls (to rule out a pattern-too-narrow false zero)

- Case-insensitive `csaf|security advisory framework|\bvex\b|product_status|known_not_affected|openvex|cyclonedx vex` over the whole of each sibling repo (excluding .ufo, .git): only the same kake line, plus unrelated noise: English/Old-English/Old-Norse dictionary and OCR text "vex" (verb "to vex"; Old Norse "vex" = grows) under kotodama-shokunin/reports/** and kotodama .scratch copies; `existsSyncSafe` substring false positives in kumitate scripts/counter-rerun.mjs; one jj working_copy tree_state binary index line in chousa (filename ScoutDocsAfter33, not content).
- Case-insensitive `csaf|\bvex\b|product_status|known_not_affected|openvex` over all of shokuknow/merge (every file type): 0 hits.
- kake S079 context: `kake-shokunin/corpus/SOURCES.md:87` S079 = securitytxt.org (tier A); the CSAF mention is a one-clause aside inside the security.txt entry, not a source for CSAF itself.
- Lane's own state: `git ls-tree -r --name-only HEAD | grep -ic csaf` in kasegi-shokunin = 0; no `csaf`/`vex` file in corpus/knowledge (49 entries pre-round).

## Classification

| Hit | Class | Reason |
|---|---|---|
| kake security-txt-publishing.md:63 (CSAF named as a security.txt extension field, S079) | adjacent | Names CSAF only as an extension label of security.txt; carries no CSAF content: no product-status categories, no justification flags, no document structure, no CSAF spec source in kake's SOURCES.md (S079 is securitytxt.org). Does not hold F21 ground. |
| kotodama "vex" (dictionary/OCR text) | unrelated | English/Old-Norse word. |
| kumitate `existsSyncSafe` | unrelated | Substring false positive. |
| chousa jj tree_state | unrelated | Filename in binary index. |
| shokuknow/merge (all 21 lanes) | no hits | Nothing held. |

Held ground (a sibling or the merge already covers CSAF VEX product-status/justification semantics): **none**.

## Nearby adjacent ground (no CSAF/VEX terms; for context only, none overlaps F21's claimed content)

- kasegi's own `corpus/knowledge/multiparty-vulnerability-coordination.md` (upstream/downstream vendor, affected-product boundaries; line 39 mentions a "not affected"/"fixed" status check): the coordination side, from ISO 29147/30111-style sources, not the CSAF VEX machine-readable statuses.
- shokuknow/merge/kagi secret-scanning validity/severity taxonomy entries and merge/kasegi severity/disclosure entries (CVSS-like, CVE, advisory words): vulnerability-severity vocabulary, not VEX product-status.
- Other siblings' CVE/SBOM/advisory hits are audio (PipeWire source text), not security-document formats.

## Conclusion for the L1

F21 is clear ground: no sibling lane and no shokuknow merge carries CSAF, VEX, `product_status` or `known_not_affected`. The only mention (kake, `CSAF` as a securitytxt.org extension, S079) is adjacent and does not cover F21. No duplicate-ground conflict with the S055 entry `csaf-vex-product-status-and-justifications.md`. kake's S079 may be cited as a neighbour pointer only; it is not a source for the entry.

Confidence: high on the zero result (case-sensitive spec pattern plus case-insensitive widened controls over entire repos and the merge tree). Remaining unknown: nothing in scope.
