# ConnectorOverlap — cross-lane overlap scan (round-78 w1, read-only)

Seat: ConnectorOverlap-20. Date: 2026-11-05. Frozen base 0687cca8 / freeze 2d81fe845.
Axes touched: coverage (does any sibling already hold the S112 ground?), depth:verifiability (do open L0 rulings constrain how C2's S112 claims get verified?).
Method: case-insensitive regex over `/home/vgpnk/Projects/shokunin/*-shokunin/{corpus,.ufo}/**` (kasegi excluded where stated), `corpus/SOURCES.md` per lane, and `.ufo/l0-questions.md`. No lane/fleet file was edited; nothing committed; no git/jj writes. No tools installed.

## (1) `querybatch` over sibling `corpus/` + `.ufo/` — ZERO hits

20 sibling lanes searched (kagi, tabi, kengaku, kotoba, kama, kaidoku, kumitate, kake, kotodama, mado, tameshi, mori, tsukuroi, chousa, souji, revenger, lore, game-dev-2d, audio, game-dev-3d; stray `kumitate-shokinin/` has no corpus/.ufo). `(?i)querybatch` → **no matches** in any sibling.

Traversal control (why the null is a true negative): `(?i)\bosv\b` over the identical path set hits **129 files** across siblings, so the trees were walked. Breakdown of those 129 hits — none is querybatch ground:
- `kaidoku-shokunin/corpus/SOURCES.md:21` — S015, OSV **single-vuln record** `https://api.osv.dev/v1/vulns/CVE-2025-55305` (GET /v1/vulns/{id}, dataset kind). Copied verbatim into kaidoku fixtures: `corpus/lessons/round-13.md:42,59`, `corpus/evidence/round-30/c1/pypi-uv-0.13.0.json:1` (osv.dev/vulnerability links), and ~10 mirror copies under `.ufo/waves/round-{38,39,43,49}/**` fixture trees.
- `kotodama-shokunin/corpus/knowledge/linguistics/syntax-typology.md:11,32` — "OSV" = Object–Subject–Verb word order. False positive.
- `kagi-shokunin/.ufo/waves/round-31/build/ConnOverlap-headings-nonconformant.txt:514` — quotes **kasegi's own** `SCORECARD.md:1935` ("Round 50 … OSV affected-range surface"). A cross-lane citation of kasegi's surface, not independent ground.
- Remainder: kaidoku fixture mirrors of the above rows.

**Verdict per hit:** kaidoku S015 → **none** (same API family, different endpoint — GET record, not POST /v1/querybatch); kotodama → **none** (lexical false positive); kagi wave dump → **none** (cites kasegi's own registry).

## (2) Duplicate S112 check — no sibling holds the page

`(?i)post-v1-querybatch` over every lane's `corpus/SOURCES.md` (all 21 files exist and were read): the only matches are **kasegi's own** rows `corpus/SOURCES.md:123` (S111 overview) and `:124` (S112, POST /v1/querybatch). Kasegi exclusively holds the OSV.dev docs family: S080 (`:86`, osv-schema), S108 (`:120`, POST /v1/query), S111 (`:123`), S112 (`:124`); S065 (`:71`, osv-schema, status rejected).

**Verdict: none** — no duplicate-source across lanes. This is absence of adjacency, not evidence of overlap; per the seat spec, no action taken.

## (3) kasegi-relevant L0 rulings in `/home/vgpnk/Projects/shokunin/.ufo/l0-questions.md` (line numbers only)

Touching S112 / the OSV page / the staged shokuknow id, binding on this round:
- **:353** — staged `merge/kasegi` id **S112 (TC260)** collides with lane S112 (OSV querybatch, SOURCES.md:124); 82/94 staged ids collide; renumber-vs-lane-row decision OPEN. Assimilation append must stay closed this round.
- **:354** — `source-recheck.py` `anchor_verdict` uses a **four-line window** (`raw_lines[anchor-1:anchor+3]`); round-77 manifest anchors Q04/Q05 pass under it; window-vs-exact-line ruling OPEN. Governs how any S112 manifest anchor recheck is read.
- **:340** — frozen S111 manifest Q01 quote "API (1.0)" (9 chars) < MIN_QUOTE_CHARS=12 → recheck exit 2; successor-round-with-fresh-manifest (option A) vs operator re-freeze (option B) OPEN. Direct precedent for the round-78 S112 manifest shape.
- **:341** — staged S111 (NCSC) vs lane S111 (OSV overview); same collision family.
- Mass id-drift family, same open decision: **:328** (r75, 79 collisions), **:308** (r71, 75), **:307** (r70, 73).
- Older lane counter-hygiene ruling, background only: **:269** (r57 census range bases + stub-entry limb).

Other lanes' staged-shokuknow-id rulings (line numbers only, out of this round's scope): :146, :149, :150, :165, :183, :192, :205, :251, :268, :277, :304, :309, :322.

## Overlaps found (summary table)

| Lane | File:line | Kind | Verdict |
|---|---|---|---|
| kaidoku | corpus/SOURCES.md:21 (S015) + lessons/round-13.md:42,59 + evidence/round-30/c1/pypi-uv-0.13.0.json:1 | OSV single-vuln GET record, same API family | none (different endpoint, different scope) |
| kotodama | corpus/knowledge/linguistics/syntax-typology.md:11,32 | lexical "OSV" false positive | none |
| kagi | .ufo/waves/round-31/build/ConnOverlap-headings-nonconformant.txt:514 | quotes kasegi's own SCORECARD heading | none (self-citation, not sibling ground) |
| any sibling | corpus/SOURCES.md (all 21 checked) | duplicate of S112/OSV docs page | none — kasegi sole holder of S108/S111/S112 |

## Recommendation for the L1 (one line)

Proceed with C2's F54 admission on S112 scoped to the seven batch-specific clauses Q01, Q02, Q03, Q09, Q10, Q11, Q13 — no sibling lane holds querybatch or any OSV.dev docs ground (zero `querybatch` hits; 129-file OSV control sweep confirms the null) — while keeping the staged `merge/kasegi` package unassimilated (L0 :353/:341/:328/:308/:307 id-collision decision open) and reading S112 manifest anchors under the recorded four-line window rule (L0 :354), with :340's MIN_QUOTE_CHARS precedent honored when pinning quotes.
