# AttackZ1 — used-by edge map for S039/S040/S041 (wave-1 deferred seat, completed)

Seat: L1Kasegi26.AttackZ1 (read-only leaf, wave 2, round 26).
Item completed: the wave-1 deferred milestone — compute used-by edges for S039/S040/S041 from
`corpus/knowledge/*.md` `source:` headers; assert the three specified relationships; confirm no
orphan rows (census W03/E11 semantics). No tools installed (pacman paused; nothing needed).

## Method (all evidence local, read-only)

1. Enumerated all 39 `corpus/knowledge/*.md` entries (glob) and extracted every `source:`
   header line (grep `^source:` across the dir; both halves of the 39-file list were read).
2. Read `corpus/SOURCES.md` rows S032–S041 in full (including each row's `used-by` cell) and
   the two F10 entries + two F11 entries in full (headers, `ground:` lines, bodies).
3. Cross-checked the header-derived map against the registry rows' `used-by` cells.
4. Ran the read-only sources census validate as grounding for the orphan check:
   `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi`
   → `EXIT=0`, stdout only `kasegi W04 S028 …`, `kasegi W04 S029 …`, `kasegi ok <SOURCES.md>`
   (the two pre-existing W04 URL-duplicate warnings; no E09, no W03, no E11).

## Computed used-by edge map (from `source:` headers)

| Row | Header-cited by (knowledge entries) | Registry `used-by` cell |
|---|---|---|
| S039 | `vendor-disclosure-policies-as-corpus-objects.md` (source line 6), `vendor-disclosure-policy-commitments-crosswalk.md` (source line 5) | exactly those two files |
| S040 | `vendor-disclosure-policy-commitments-crosswalk.md` (source line 2) | exactly that one file |
| S041 | `iso-29147-and-30111-division-of-labour.md` (source line 2), `iso-29147-divergence-and-clause-crosswalk.md` (source line 3) | exactly those two files |

The registry `used-by` cells and the header-derived edges agree 1:1 for all three rows, and for
every other mined row checked (S001–S015, S018, S029–S038; each cell names exactly the entries
whose `source:` headers cite that row — no cell over- or under-lists).

## Assertions (all PASS at header granularity)

- **S041 used-by = the two F11 entries** — PASS. The F11 row in `corpus/README.md` lists
  exactly `knowledge/iso-29147-and-30111-division-of-labour.md` and
  `knowledge/iso-29147-divergence-and-clause-crosswalk.md`; both carry `source: S041` in their
  headers, and no other knowledge entry cites S041 in a header (grep `S041` across the dir hits
  only these two files).
- **S040 used-by = the F10 crosswalk** — PASS. The F10 crosswalk entry
  `vendor-disclosure-policy-commitments-crosswalk.md` is the only entry whose header cites S040.
- **S039 used-by = both F10 entries + none of the F11 entries** — PASS at header granularity.
  Both F10 entries (`vendor-disclosure-policies-as-corpus-objects.md` and
  `vendor-disclosure-policy-commitments-crosswalk.md`) cite S039 in headers; neither F11 entry
  carries S039 in its `source:` header (both F11 headers are S041-only).

## Orphan-row check (PASS)

- **No dangling header citations:** the union of `S###` ids in knowledge headers is
  {S001, S003, S006, S009, S013, S018, S029, S031, S032, S033, S034, S035, S036, S037,
  S038, S039, S040, S041} — every one is a registered SOURCES.md row; no header cites an
  unregistered id.
- **No unmined orphans:** every `mined` row has a non-`—` used-by cell naming an existing
  knowledge file (census W03 would fire otherwise); the `—` cells are exactly the queued
  (S016, S017, S019–S025) and rejected (S026–S028) rows, which is the designed state.
- **All used-by paths exist on disk** (E11 would fire otherwise), including the four files used
  by S039/S040/S041.
- **Census confirmation:** `validate` exits 0 with only the two pre-existing W04 warnings
  (S028/S029 duplicate URL across scopes) — consistent with the round-26 lesson §Fixes 5
  expectation at round end.
- Note: QUALITY R9 (numerical erratum) is not the rule that governs orphans; the operative
  definitions are the census W03 (mined row with used-by `—`) and E11 (used-by path missing on
  disk), which is the semantics used above.

## Nuance found (state explicitly, not smoothed)

Body-level citations extend the header map: `iso-29147-and-30111-division-of-labour.md` (an
F11 entry) quotes S039 three times and S040 once in its body (quote-table rows `hitachi-step1/2/3-*`
and `cisco-iso-29147-2018`, plus its rejected-over-generalization section), and
`iso-29147-divergence-and-clause-crosswalk.md` mentions S040 as a pointer (参考2 example, "pointer
only"). So at **body** granularity, S039 and S040 have an additional used-by edge to the F11
division-of-labour entry. This does **not** contradict the stated assertions (which are scoped to
the Q1 `source:` header field — the same granularity the registry `used-by` column and R12's
`--source` coverage use), but any future instrument that measured used-by from body quotes (Q3
quote tables) would count these edges too.

## Risks

- The S039/S040 → F11 body edges mean a body-granularity used-by audit would report a larger set
  than the registry column; the registry cell is the canonical census input, so this is a
  definitional note, not a defect.
- R12 measures `recheck:` `--source` ids against header `source:` ids; the F11 entries' recheck
  lines cover exactly S041, so no R12 gap from the S039/S040 body quotes.

## Verification

- Header grep outputs (all 39 files) and full reads of the four entries and registry rows are the
  evidence; the census validate run printed `EXIT=0` with the two W04 warnings quoted above.
- No unrun check is claimed; no production edit was made (report files in `wave2/` only).
