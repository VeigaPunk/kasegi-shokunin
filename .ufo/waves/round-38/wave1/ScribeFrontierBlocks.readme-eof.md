```

Correction (round 38): corpus/README.md L399-L454 — the whole round-37 append — carry misplaced receipt scaffolding copied from `.ufo/waves/round-37/wave1/ScribeFrontierAmendments.md`: receipt property and validation tables, a "Validation on a scratch mirror" section with its check table, and a stray fence at L426 that leaves the rest of the file inside a code block; the intended round-37 block was 27 lines (sha256 2ebd8cd2881b020cb0e234658adf132cf4741c1d226e1d7c267f7d71c5b7e97b, the bytes of that receipt's §3 "Deliverable B — `corpus/README.md` end-of-file block"), of which only L400-L425 landed unchanged — L399 is a blank line where the block's `## Round-37 admission — coverage map row and Frontier F20 (appended 2026-10-26)` heading belonged; the fence opened at L426 is closed by this block, whose first line is the closing fence, and L426-L454 are to be read as not part of the corpus index.

## Round-38 admission — coverage map row and Frontier F21 (appended 2026-10-26)

The coverage map above is not edited in place (R6): the round-38 entry
`knowledge/csaf-vex-product-status-and-justifications.md` (Frontier F21, source S055;
source basis: the OASIS CSAF TC's own normative text, the CSAF 2.0 OASIS Standard at
https://docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.html — the standard document itself, not
a summary page or the TC's home — captured 2026-10-26T18:25:51Z, HTTP status 200, 272441 bytes /
5146 lines, sha256 63c8ad5271ef5dfb7edcf2c65b4555a2d81a82682fe4d31058d542880e11cd42, under
`corpus/source-snapshots/round-38/`) is recorded here as an appended amendment so every existing
line keeps its number. The coverage-map row is appended here rather than inserted into the map, and
the F21 frontier row is listed here on the same table shape as the frontier above.

| Area | Entry | Source basis |
|---|---|---|
| VEX product-status categories and not-affected justification flags (round 38) | knowledge/csaf-vex-product-status-and-justifications.md | S055 — public primary, opened 2026-10-26 |

| id | topic | status | entry | sources | next |
|---|---|---|---|---|---|
| F21 | OASIS CSAF v2.0 (Common Security Advisory Framework) — VEX product-status categories and machine-readable not-affected justification flags | admitted | knowledge/csaf-vex-product-status-and-justifications.md | S055 | Read a product's affect status from the vendor's own VEX block, not a severity score: "The main purpose of the VEX format is to state that and why a certain product is, or is not, affected by a vulnerability" (S055.txt:2135), and every vulnerability item MUST carry at least one of fixed, known_affected, known_not_affected or under_investigation in product_status (S055.txt:2844). known_not_affected is not a bare label — "an impact statement SHALL exist as machine readable flag" (S055.txt:2152) drawn from the labels that "reflect the VEX not affected justifications" (S055.txt:1762), such as vulnerable_code_not_in_execute_path, "The affected code is not reachable through the execution of the code, including non-anticipated states of the product." (S055.txt:1767). Keep it distinct from CVSS severity, KEV status, EPSS likelihood and SSVC decisions: CSAF states whether the vendor's own product is affected and why, not how severe the vulnerability is or how likely its exploitation is — this capture defines no severity scale. |

[r38 amendment, appended 2026-10-26] The parenthetical above records the round-26 frontier state
and each later amendment paragraph states its own round; those are retained as history, not
rewritten (R9): at round 38 the frontier stands at **21/21 admitted** — F01-F08 at round 23, F09
at round 24, F10 at round 25, F11 at round 26, F12 at round 28, F13 at round 29, F14 at round 30,
F15 at round 31, F16 at round 33, F17 at round 34, F18 at round 35, F19 at round 36, F20 at round
37, F21 at round 38. The 0/18 sentence is untouched: the lost-domain denominator still holds 0 of 18
surfaces present, and the frontier count stays outside it.

