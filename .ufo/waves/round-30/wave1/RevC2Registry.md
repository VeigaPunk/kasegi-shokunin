# RevC2Registry — C2 registry review

## Finding

- **High — C2 census/used-by acceptance fails on measured bytes.** `corpus/SOURCES.md` rows S046 and S047 both cite `corpus/knowledge/japanese-severity-vocabulary-and-impact-model.md`, but that path is absent from the current `corpus/knowledge/` listing. Ran `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi`; it emitted `E11 S046 missing used-by ...` and `E11 S047 missing used-by ...`, and returned `census_exit=1`. The F14 knowledge entry must exist before this claim passes; no source change made by reviewer.

## Registry checks

- Parsed S046/S047 in `corpus/SOURCES.md`: each has the 11 header columns (10 delimiters), no cell-internal `|`, and valid-looking enums (`docs`, tier `A`, status `mined`, opened date `2026-10-25`, recheck `180d` / `90d`). IDs are distinct and continue the sequence after S045. The census did not report duplicate IDs or invalid row shape/enums; its only new errors were the two E11 missing used-by paths.
- Read `git diff a94871315cafa368f79c17d8c62d71fddd967986 -- corpus/SOURCES.md`: exactly two added data rows (S046/S047) and three appended Registry changes lines; no old row was modified. Working-tree bytes measured: SHA-256 `a126a5f339323d5ae417a944d163d75a0427d9c77a5a330308e193dc7b81d927`.
- The Registry changes log states S046 staged S049 → landed S046, opened `2026-10-23` → `2026-10-25`, capture-based anchor rewrite and F14-only used-by; S047 staged S050 → landed S047, date adjustment, `180d` → `90d`, capture-based anchor rewrite and F14-only used-by. It also records no status/recheck/used-by changes for pre-existing rows and 45 → 47 rows (R8 old→new logging present for both adopted sources).

## Residual risk / verification gaps

- Census is not green; therefore C2's required census exit 0 is unmet on these bytes. Re-run after the cited knowledge entry is present. No other census acceptance (frontier/harness/rechecks) was independently verified here.
