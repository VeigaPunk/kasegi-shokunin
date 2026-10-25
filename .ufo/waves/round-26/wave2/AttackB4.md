# AttackB4 — README variant sanity (round-26 wave 2)

Seat: `L1Kasegi26.AttackB4` (leaf, read-only).
Item: falsify the claimed AFTER state of `corpus/README.md` (F11 row; counts 37→39).
Verdict: **PASS with two scoped observations** — all enumerated checks hold; two consistency notes (header count, coverage-map row) are recorded for the scribe/amender.

## Checks (all executed on /home/vgpnk/Projects/shokunin/kasegi-shokunin)

| # | Check | Result |
|---|---|---|
| 1 | F11 row exactly once | PASS — `| F11 | ISO/IEC 29147/30111 division-of-labour meta | admitted | knowledge/iso-29147-and-30111-division-of-labour.md, knowledge/iso-29147-divergence-and-clause-crosswalk.md | S041 | …` appears exactly once, at line 212 (only frontier-table row). |
| 2 | awk frontier counter = 11 | PASS — `awk -F'|' '/^\| F[0-9]+ \|/ {n++}'` ⇒ n=11 (F01…F11, in order). |
| 3 | Entry cell paths exist | PASS — both exist and are non-empty: `corpus/knowledge/iso-29147-and-30111-division-of-labour.md` (54 lines), `corpus/knowledge/iso-29147-divergence-and-clause-crosswalk.md` (67 lines); both carry `source: S041`, `verified-at: 2026-10-25`, and a `recheck: source-recheck.py --manifest …round-26/manifest.json --source S041` command. |
| 4 | Sources cell = S041 | PASS — F11 sources cell is exactly `S041`; matches SOURCES.md row S041 (JPCERT/CC 2026 P-guideline PDF). |
| 5 | No stray F12 | PASS — no F12 or any higher F-id anywhere in README (grep `F1[1-9]|F[2-9][0-9]` matches only the F11 row and the frontier footer sentence). |
| 6 | F01–F10 untouched vs round-25 map | PASS — `git diff 98261eb -- corpus/README.md` shows the ENTIRE delta is: (a) +1 line = F11 row after F10; (b) footer sentence `10/10 admitted at round 25` → `11/11 admitted at round 26; F01-F08 at round 23, F09 at round 24, F10 at round 25, F11 at round 26`. F01–F10 rows (and all coverage-map/known-gaps content) byte-identical to round-25 commit 98261eb. |

## Observations (consistency, not check failures)

- **O1 (moderate): header count is stale — 37, not 39.** The admission header (line 5) ends at the r25 correction: *"the round-25 entry count is 37 — F10 admits two entries re-grounded from public sources S036-S040 captured 2026-10-25"*. There is NO r26 correction updating the count. Canonical count is 39 (F11 admits two entries → 37+2=39; `corpus/instruments/knowledge-expected.txt` contains 39 entries — 2 header comment lines + 39 paths = 41 non-blank lines). The string `39` appears nowhere in README; the only round-26 count reference is the frontier footer (11/11). Header should gain an r26 correction (37→39) for consistency with the expected list and SOURCES/registry counts.
- **O2 (minor): F11 has no Coverage-map row.** Every prior frontier item has a corresponding coverage-map row (F01–F05 → lines 37–41; F06–F08 → 45–47; F09 → 48–49; F10 → 50–51). F11's two entries (`iso-29147-and-30111-division-of-labour.md`, `iso-29147-divergence-and-clause-crosswalk.md`) have no round-26 coverage row. The frontier table is the only index of S041.

## State note (informational)

- The README edit is **uncommitted**: `git status --porcelain -- corpus/README.md` ⇒ ` M corpus/README.md`; HEAD `1b076fa` still contains no F11 (grep F11 in HEAD version = 0). This matches the lane's pre-existing stalled-rebase / working-tree-only state (recorded in README known-gaps) — not a wave defect, but the landed claim depends on the working tree, not a commit.

## Residual risk / verification gaps

- The semantic body of the two iso-29147 entries (beyond grounding headers) was not reviewed — out of scope for this README-sanity item. The source snapshot `corpus/source-snapshots/round-26/S041.txt` is referenced by both entries and was not re-validated here (recheck command supplied in-file).
- SCORECARD/SOURCES rows were read only to cross-check the S041 reference; no row-by-row audit was performed.
- No installs made; no tools used beyond git/awk/grep/read.
