# RevD1D2 — review of the SCORECARD.md corrections (D1 lane-hash fill, D2 density-row erratum)

Round 35 wave 1, lane base `3266c9937b03062d9bbc2f436e20820115ed179c`, claims-freeze `617496b9c6e92bc671e7e78b83df69a04470d0e9`, HEAD at review time `da2d3c6` (round-35: wave-1 spec + dispatch). Scope: the three limbs of my item — placeholder count → 0, the c1c6a5f correction, the depth:density-row erratum with stale-row bytes untouched.

## Report

All commands run in `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (read-only review; the only lane writes are this receipt). Scratch `/fast/scratch/hyaku/kasegi-r35/RevD1D2/` (removed before yield; no tool installs — none needed).

### Final byte state reviewed

- `SCORECARD.md` sha256 `51337bf1fd5da7a5aebb626fe8c5fd520cce40209d79537324cf9d08a990efc7`, 1261 lines, stable across reads at 2026-10-26T06:43:57Z and 06:46:08Z.
- `.ufo/waves/round-35/claims.json` sha256 `fe0dae8957c38f9c697b1b851a528bdf516f949f6ee3ba1ca2846e61d1ea2982` (87 lines).
- `corpus/lessons/round-34-verifier-spotcheck.md` sha256 `dc10c6501a1992abb08880b1f8d8477992db70b03b3b3f985557036d0752748e` (D1/D2 source, §6).

### Limb 1 — placeholder count

```
$ grep -c 'filled by the L1' SCORECARD.md      -> 0   (grep exit 1 = no match)
$ grep -c 'the L1 fills' SCORECARD.md          -> 0   (exit 1)
$ grep -c 'LANE_HASH' SCORECARD.md             -> 0   (exit 1)
$ grep -c 'c1c6a5f826d2425446347173de527c42991b78b0' SCORECARD.md -> 3 (exit 0)
```

Kill-rule spellings (claims.json:17: "`<LANE_HASH>` still present" / "`filled by the L1` placeholder prose still present") are all 0. The three c1c6a5f citations: preamble `SCORECARD.md:1130`, closing line `:1242`, Correction paragraph `:1250`. Before-state at HEAD/617496b/c1c6a5f: exactly 1 occurrence (`git grep -n 'filled by the L1' HEAD -- SCORECARD.md` → `HEAD:SCORECARD.md:1240`), matching claims.json:27 "carries 1 'filled by the L1' placeholder line, 0 citations of ... c1c6a5f".

### Limb 2 — correction names c1c6a5f and is appended

Appended paragraph `SCORECARD.md:1250-1253`: "Correction (round 35): the two lane-commit placeholder sentences above (the preamble's and the closing paragraph's) were replaced with the round-34 final lane hash `c1c6a5f826d2425446347173de527c42991b78b0` (the round-34 lane tip at its non-author closure). Neither placeholder spelling occurs in this file any more; ...". Both placeholder sentences are replaced in place by the hash (`:1130`, `:1242`), per D1's spotcheck fix clause ("append a correction naming `c1c6a5f826d...`, and widen the R1 check to placeholder prose" — round-34-verifier-spotcheck.md §6 D1).

Hash identity verified against the DAG: `git log --oneline` = `da2d3c6 → 617496b → 3266c99 (round-34 verifier spot-check, non-author) → c1c6a5f (round-34: late ExecRegressionC1 receipt + lesson/LOG post-commit errata) → 4eafa84`; `git rev-parse --verify 4b0a9f2^{commit}` → `4b0a9f29a8797828fb711faed80ee151afdf5117` ("round-34: C1 R1-R9 closure suite + kill-rule-check; C2 F17 ... wave1 receipts (65 seats)"); `git diff 4b0a9f2 c1c6a5f --stat` = 3 files, +521/−2 (LOG.md, round-34 lesson, late receipt) — c1c6a5f is the round-34 tip content plus post-commit errata, exactly as the Correction calls it.

**The item's gloss "0 deletions in the round-34 section per `git diff --numstat`" is FALSE — and unsatisfiable:**

```
$ git diff --numstat HEAD -- SCORECARD.md   ->  33  15  SCORECARD.md
$ git diff --numstat 617496b -- SCORECARD.md ->  33  15  (same)
$ git diff --numstat 3266c99 -- SCORECARD.md ->  33  15  (same)
```

Both hunks (`@@ -1126,17 +1126,18 @@`, `@@ -1237,7 +1238,24 @@`) lie inside the round-34 section (lines 1121→EOF 1261; round-34 is the file's last section). The 15 deletions are the two placeholder paragraphs (one of which literally contains the phrase `filled by the L1`, so reaching count 0 *requires* deleting its bytes — "0 deletions" and "count 0" are mutually exclusive for that line). The canonical frozen claim (claims.json:37) requires only "count 0 with appended correction naming c1c6a5f" — **met**; the 0-deletions wording exists only in my dispatch item and cannot be read as a work requirement.

### Limb 3 — density-row erratum, stale row untouched, 201.2 real

- Erratum appended at `SCORECARD.md:1246`: "Erratum (round 35): the round-34 depth:density row measured 0 changed SKILL/PROVINCE lines and mean 201.7; at the tip each file had +1 appended correction line and the measured density mean is 201.2 (unchanged instrument, same definition)." — matches D2 (spotcheck §6: "Where: `SCORECARD.md:1145` ... Fix: append a correction") and claims.json:38.
- **Stale row bytes untouched:** the round-34 `depth:density` row (worktree `:1146`) hashes identically in the worktree and the c1c6a5f blob:
  `d1688a3ba687c0ed0315c8ec37a56a11d61bb196f3244a773e5912b184f743f2` both sides (count 1 each). Zero deletions of that row.
- **Byte-binding of the two means** (erratum's Measurement state, `:1248-1255`), verified:
  - `git show 206e510:SKILL.md` → sha256 `b11b60857986c3d7…`, 1090 lines; `PROVINCE.md` `b57de5d9517d0ba6…`, 74 lines.
  - `git show 3266c99…:SKILL.md` → `ba5ebe5d9417b180…`, 1091 lines; `PROVINCE.md` `b4bb5fee0a37cb2a…`, 75 lines. (c1c6a5f's blobs are identical to 3266c99's; `git diff --numstat c1c6a5f da2d3c6 -- SKILL.md PROVINCE.md` = empty.)
  - `git diff --numstat 206e510 4b0a9f2 -- SKILL.md PROVINCE.md` → `1 0 PROVINCE.md`, `1 0 SKILL.md`; the added lines are the `[r34 Frontier amendment, appended 2026-10-26, end-of-file append per R6]` (PROVINCE) and `[round-34 correction, appended 2026-10-26, end-of-file append per R6]` (SKILL) lines — the "+1 appended correction line" per file, matching the erratum's `1090a1091` / `74a75`.
- **Instrument re-run** (committed `corpus/instruments/density.py`, unchanged, exit 0 both):
  - on the 206e510 blob: `# Density census — rev-2017 (1090 lines, 25 blocks)` / mean **201.7** / `Total path-citation instances: 710 across 25 blocks.`
  - on the 3266c99 blob: `# Density census — rev-2012 (1091 lines, 25 blocks)` / mean **201.2** / `Total path-citation instances: 711 across 25 blocks.`

Both means reproduce exactly; the erratum's numbers are measured facts, not assertions.

## Findings by severity

**PASS on both frozen limbs.** D1: count 0 + appended correction naming c1c6a5f ✓ (claims.json:37). D2: appended erratum naming 201.2 with the stale row byte-identical to the c1c6a5f blob ✓ (claims.json:38). Kill-rule spellings 0 ✓.

1. **Minor (item/claims gloss, not the work):** "0 deletions in the round-34 section per `git diff --numstat`" is false (33/15, all hunks in the round-34 section) and logically incompatible with D1's own kill rule (the closing placeholder line contains the counted phrase). The frozen claims.json imposes no such requirement; the append-only invariant correctly attaches to the stale density row only, where it holds.
2. **Minor (disclosure precision in the landed text):** the Correction's closing claim "Nothing else in this section changed." is overbroad. Besides the two placeholder sentences, the preamble's posture sentence was semantically rewritten — old: "This section is written at the wave-1 integration state ..., claims no lane-commit hash, and deliberately introduces no placeholder token — round-33 R1's defect was a published placeholder, the C1 counter reads that count as 0, and nothing here moves it."; new: "... and originally carried the placeholder prose this hash replaces; round-33 R1's defect recurred here in sentence form, which the round-34 R1 check missed because it matched only the angle-bracket lane-hash marker, not this prose form — ...". The rewrite is truthful and arguably mandatory (the old sentence self-falsifies once a hash is filled) and adds the correct root cause, but the Correction paragraph should name it. The receipt-list and subject sentences are rewrap-only (verified word-identical to HEAD:1128-1140).
3. **Observation (positive):** the landed text avoids quoting either placeholder spelling ("angle-bracket lane-hash marker", "Neither placeholder spelling"), which is what keeps the kill-rule counts at 0. Per-contract, but brittle by construction: any future verbatim quote of those strings in SCORECARD re-trips the count.

## Residual risk and verification gaps

- **Live churn:** my first read (~06:39Z) found `grep -c 'filled by the L1'` = **2** in the working tree mid-edit (roster shows ExecD1Markers replacing the second placeholder at that moment); later reads are stable at 0 (sha256 `51337bf1…` at 06:43:57Z and 06:46:08Z). My verdict binds to that snapshot; the L1 must re-run the counting_commands on the quiescent tree at commit time.
- `4b0a9f2` is a jj-evolved commit off the first-parent line (resolves via cat-file, not reachable by `git log HEAD`); the erratum cites it correctly as the closing commit — noted only as DAG shape.
- Not in my scope, not run: `r35-defect-closure.sh` / `--selftest` (C1 suite seats), D3–D7 limbs. No LSP server exists for markdown prose; verification used git blob arithmetic plus an instrument re-run instead of grep-only claims.
