VERDICT: BROKEN

# R46bW2MutGate1 — single-edit mutants of `corpus/instruments/r46-f29-gate.py` (round 46 attempt 2, wave 2)

## Scope and artifacts
- Instrument attacked: `corpus/instruments/r46-f29-gate.py`, sha256 `5d192dfd66fa59bbc271f800e698e28e2a56fad319fa080adee5ca4ed3699932` (gate v1.1). Byte-identical to `git show 96379ae:corpus/instruments/r46-f29-gate.py` and to the lane worktree file.
- Positive tree (landed): **96379ae**, the wave-1 integration commit at lane HEAD. The item text names fe0f56b; fe0f56b is the freeze commit and an ancestor of 96379ae. At fe0f56b the F29 entry, S074 row and README row do not exist, so fe0f56b cannot be the positive. It is used below as a negative control.
- Export: `git archive 96379ae corpus | tar -x` into scratch (9.0 MB corpus). Scratch removed on exit. All outputs below were produced by running the gate, not inferred.
- Gate invocation: `python3 <gate> --root <tree> --work <scratch>`. Each mutant was a copy of the gate with one exact-substring replacement (asserted unique in the landed bytes), with `source-recheck.py` copied beside it (the gate resolves it from its own directory).
- Not touched: git, jj, index, MANIFEST.json, .ufo/state, fleet root, sibling lanes, ~/.local/bin. No commit, no push, no live fetch. No subagent or background work.

## Controls (do-nothing discrimination)
1. Unmutated gate on the landed positive (96379ae):
   ```
   gate H1 pass=1 read=rows=29 admitted=29 F29=admitted
   gate H2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 full=4/4 table-rows=19 xrefs=7/7 anchored=1
   gate H3 pass=1 read=row-S074=ok
   gate H4 pass=1 read=recheck-rc=0 quotes-ok=9 frozen-cores-missing=0
   gate H5 pass=1 read=spans=45 located=45 failed=0 uncited=0 cores=5/5
   gate H6 pass=1 read=knowledge=66 entries=66 nested-md=66 base-intact=1 entry-bytes-ok=1 symlinks=0
   gate H7 pass=1 read=census-rc=0 ok-line=1
   f29-gate fixed=7/7 exit=0      (rc=0)
   ```
2. Null mutant (gate + one appended comment line) on the positive: `f29-gate fixed=7/7 exit=0` (rc=0). The harness does not flip on a no-op edit.
3. Negative: unmutated gate on the freeze tree fe0f56b: `gate H1 pass=0 read=rows=28 admitted=28 dup=0`, H2/H5/H6 `entry-absent`, H3 `hits=0`, H4 `pass=1`, H7 `pass=1`, then `f29-gate fixed=2/7 exit=1` (rc=1). The v1 gate shipped at fe0f56b gives the same `fixed=2/7 exit=1`.

## Mutant set (26 single edits; 7 strengthening, 19 weakening)
Strengthening (K) must go red on the positive. All 7 did:

| id | limb | edit (landed text → mutant text) | landed output |
|---|---|---|---|
| K1 | H1 | `len(rows) != 29` → `!= 30` | `gate H1 pass=0 read=rows=29 admitted=29 dup=0`; `fixed=6/7 exit=1` |
| K2 | H3 | `row[7] != "mined"` → `!= "rejected"` | `gate H3 pass=0 read=bad=status`; `fixed=6/7 exit=1` |
| K3 | H6 | `len(names) == 66` → `== 65` | `gate H6 pass=0`; `fixed=6/7 exit=1` |
| K4 | H7 | census ok regex `\tok\t` → `\tbad\t` | `gate H7 pass=0 read=census-rc=0 ok-line=0`; `fixed=6/7 exit=1` |
| K5 | H5 | quote word cap `<= 25` → `<= 5` | `gate H5 pass=0 read=spans=45 located=2 failed=43 uncited=0 cores=0/5`; `fixed=6/7 exit=1` |
| K6 | H4 | `oks >= 8` → `oks >= 10` | `gate H4 pass=0 read=recheck-rc=0 quotes-ok=9 ...`; `fixed=6/7 exit=1` |
| K7 | H2 | `verified-at` searched in `head` → `head[:2]` | `gate H2 pass=0 read=source=1 verified-at=0 ...`; `fixed=6/7 exit=1` |

Weakening (W) edits are expected to stay green on the positive, because the positive also satisfies the stronger clause. Under the instruction "every mutant that keeps the marker must flip red on the landed tree", all 19 are survivors on the positive. Each was then graded on a scratch counterexample tree (copy of the landed export plus one defect), original vs. mutant:

| id | limb | weakening (landed → mutant) | survives positive? | counterexample tree (scratch, edit applied to the landed copy) | original | mutant | exit mutant |
|---|---|---|---|---|---|---|---|
| W1 | H1 | `or dup:` removed from the row-count line | yes (rc 0, 7/7) | README row `\| F08 \|` → `\| F07 \|` (ids F01–F07, F07, F09–F29; still 29 rows, 29 admitted, one F29 line) | `gate H1 pass=0 read=rows=29 admitted=29 dup=1` | `gate H1 pass=1 read=rows=29 admitted=29 F29=admitted` | **0 (7/7) false green** |
| W2 | H1 | `adm != 29` → `adm < 28` | yes | README F20 status `admitted` → `proposed` | `gate H1 pass=0 read=rows=29 admitted=28 dup=0` | `gate H1 pass=1` | **0 false green** |
| W3 | H1 | `anywhere != len(rows)` → `anywhere < len(rows)` | yes | append line `\|F30\|ghost row\|admitted\|` after the F29 row (visible to the regex, not parsed) | `gate H1 pass=0 read=F-rows-visible=30 parsed=29 ...` | `gate H1 pass=1` | **0 false green** |
| W4 | H2 | `len(rows) >= 6` → `>= 1` | yes | entry table reduced to G1–G3 | `gate H2 pass=0 ... table-rows=3 ...` | `gate H2 pass=1 ... table-rows=3 ...` | **0 false green** |
| W5 | H2 | cell-word floor `>= 2` → `>= 1` | yes | table reduced to G15–G19 (5 valid) plus `\| G20 \| Why \| short (\`S074.txt:13\`) \|` | `gate H2 pass=0 ... table-rows=5` | `gate H2 pass=1 ... table-rows=6` | **0 false green** |
| W6 | H2 | `h == "verified-at: "+VERIFIED_AT` → `h.startswith("verified-at: ")` | yes | entry line 2 `verified-at: 2026-10-29` → `verified-at: 2025-06-01` | `gate H2 pass=0 ... verified-at=0` | `gate H2 pass=1 ... verified-at=1` | **0 false green** |
| W7 | H2 | `recheck:` count `== 1` → `>= 1` | yes | second line `recheck: cadence note lives in the source row` added after line 2 | `gate H2 pass=0 ... recheck=0` | `gate H2 pass=1 ... recheck=1` | **0 false green** |
| W8 | H3 | `row[8] != VERIFIED_AT` ("opened") check disabled | yes | SOURCES S074 opened `2026-10-29` → `2026-09-01` | `gate H3 pass=0 read=bad=opened` | `gate H3 pass=1 read=row-S074=ok` | **0 false green** |
| W9 | H3 | tier `!= "A"` → `not in ("A","B")` | yes | S074 tier `A` → `B` | `gate H3 pass=0 read=bad=tier` | `gate H3 pass=1` | **0 false green** |
| W10 | H3 | `len(c) == 11` → `>= 11` | yes | append ` extra \|` to the S074 row (12 cells) | `gate H3 pass=0 read=...hits=1` | `gate H3 pass=1 read=row-S074=ok` | 1 — limb flips, gate still red via H7 (census rejects 12-cell row: `gate H7 pass=0 read=census-rc=1 ok-line=0`) |
| W11 | H4 | manifest pin check disabled | yes | append `\n` to `manifest.json` | `gate H4 pass=0 read=manifest-not-the-pinned-bytes` | `gate H4 pass=1 read=recheck-rc=0 quotes-ok=9 ...` | **0 false green** |
| W12 | H4 | `anchor` floor `>= 7` → `>= 1` | yes | none — **equivalent under PINS**: the anchor set is read only from `manifest.json`, which H4 pins to sha256 `46e8077a…`; the pinned manifest has 8 distinct anchors (`[10,13,17,24,25,25,26,31,38]`), so `>=7` and `>=1` agree on every input that reaches the comparison | — | — | equivalence (proof given) |
| W13 | H5 | span width `b - a <= 11` → `<= 41` | yes | entry line 12 first cite `(\`S074.txt:3\`)` → `(\`S074.txt:3-20\`)` | `gate H5 pass=0 read=spans=45 located=44 failed=1 uncited=0 cores=5/5` | `gate H5 pass=1 read=spans=45 located=45 failed=0 ...` | **0 false green** |
| W14 | H5 | `len(cores) == 5` → `>= 4` | yes | remove every span carrying core 5: entry lines 20, 46, bullet 110–113, item 137–138 (the core also wraps across lines, so a one-line deletion is not enough) | `gate H5 pass=0 read=spans=41 located=41 failed=0 uncited=0 cores=4/5` | `gate H5 pass=1 read=spans=41 ... cores=4/5` | **0 false green** |
| W15 | H6 | size floor `>= 3000` → `>= 1000` | yes | replace entry (15,320 bytes) with a 2,762-byte entry that is valid on every other limb (6 table rows, 8 located quotes, 5/5 cores, 2/2 refs, 4 sections full) | `gate H6 pass=0 read=... entry-bytes-ok=0`; `fixed=6/7 exit=1` | `gate H6 pass=1`; `fixed=7/7 exit=0` | **0 false green** (the size floor is the only clause rejecting this entry; see limitations) |
| W16 | H7 | `reg != 1` → `reg < 1` | yes | append `## Registry` heading to SOURCES.md | `gate H7 pass=0 read=registry-sections=2 (...)` | `gate H7 pass=1 read=census-rc=0 ok-line=1` | **0 false green** (census accepts the duplicate; `reg != 1` is the only guard) |
| W17 | H7 | symlink check disabled | yes | `corpus` → symlink to `corpus-real` | `gate H7 pass=0 read=census-input-is-a-symlink` | `gate H7 pass=1 read=census-rc=0 ok-line=1` | 1 — limb flips, gate still red via H6 `symlinks=1` |
| W18 | H3 | `not urls or any(x != URL …)` → `not urls` | yes | S074 source cell gains a second URL `(mirror https://go.example/r)` | `gate H3 pass=0 read=bad=url` | `gate H3 pass=1 read=row-S074=ok` | **0 false green** |
| W19 | H3 | `snap_sha not in row[5]` ("anchor-sha") disabled | yes | S074 anchor cell: sha256 replaced by `(sha omitted)` | `gate H3 pass=0 read=bad=anchor-sha` | `gate H3 pass=1 read=row-S074=ok` | **0 false green** |

Totals on the landed positive: 7 kills (K1–K7); 19 survivors (W1–W19). Of the 19, 16 are exit-level false greens with a counterexample tree (W1–W9, W11, W13–W16, W18, W19, plus W15 as a size-only case); W10 and W17 flip their own limb but the gate stays red through H7 or H6; W12 is equivalent under the pins.

## Findings (false-green class)
F1. Every weakening of a floor, count or equality in H1–H7 that the landed positive satisfies is invisible on the positive. Only the counterexample trees show them. Reproduce any row with: copy the landed export, apply the listed edit, run the original and the mutant gate, compare the `gate H<n>` line.
F2. The H2 table floor (W4) and cell-word floor (W5) accept a 3-row and a 5+1-row table as passing. Only the `>= 6` row count and the `>= 2` cell count separate a thin table from a valid one.
F3. H3 accepts tier `B` (W9), an unpinned `opened` date (W8), a second URL in the source cell (W18), and no anchor sha (W19). Each relaxes a stated rule in the row contract.
F4. H2 accepts a wrong `verified-at:` date (W6) and two `recheck:` lines (W7). The second recheck line is a cadence-cell conflict the gate should catch.
F5. H1 is blind to a duplicate id other than F29 (W1). The `dup` clause is the only guard for that tree. This contradicts the R50 disclosure (a), which says any tree that duplicates the row also trips `dup`/`entry-shared`. That holds only for a duplicate of F29 itself, and the raw one-line F29 check catches that; a duplicate of another id does not trip either.
F6. H1 accepts an admitted count of 28 (W2) and a stray F-row visible to the regex but not parsed (W3, a 30-visible / 29-parsed ghost row).
F7. H3 relaxed to `>= 11` cells (W10) passes the limb with a trailing extra cell. R50's disclosure (c) says the 9-cell relaxation is closed by construction; that is not true of the 11+ direction. The gate is still red only because census rejects the extra cell (H7), so the gate's exit code depends on the census for this defect.
F8. H5 accepts a span of width up to 41 lines (W13), and accepts four of five frozen cores (W14). The R50 disclosure (e) covers the located-count floor; it does not cover the core floor or the width limit.
F9. H6 accepts a 2,762-byte entry (W15) that is valid on every other limb. The size floor is the only clause rejecting it. If a compact entry is meant to pass, the 3000-byte floor is an over-strict false red; if not, it is the only size guard and it is at 3000 with no content test behind it. Either way the floor is not redundant.
F10. H7 accepts a duplicated `## Registry` heading (W16). The census does not see it, so `reg != 1` is the sole guard. R50 disclosure (f) calls H7 census-dependent; for this defect the lane-side clause is the only guard, and it is weakened.
F11. H7 symlink check removed (W17): the census still returns ok for `corpus` as a symlink. The gate stays red only through H6's `symlinks` clause (verified: `gate H6 pass=0 ... symlinks=1`), so H6 is the second line of defence for this defect.

## Limitations
- Only single-edit mutants on v1.1 (`5d192dfd…`). The R50 set (v1, `a1091e24…`) was not rerun, per the item.
- W15's counterexample is a short but otherwise valid entry. It shows the size floor is the only clause that rejects it, not that the entry is junk; the verdict on W15 is a judgment on which way the floor should go.
- W12's equivalence rests on the pins (`manifest.json` sha256 `46e8077ac89edb0335711826ecb7abf3a1b7eefedc7108c3f6d936135481569f`, `source-recheck.py` sha256 `fd2e01e88c8c45a949f48d67b3154ae87a95aeba0b6a9c42fbf64641b5b9c003`). Not separately verified beyond the 8-anchor count and the pin check in the gate itself.
- The census (`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`) was used as-is; not mutated, not inspected beyond rc/ok-line.
- Counterexample trees are not committed; they were built in scratch and removed.
- Limb-level results were read from the gate's own output lines; I did not re-derive each limb's logic beyond the edit list above.
- No installs. No live fetch. No credentials. No live-target testing.
