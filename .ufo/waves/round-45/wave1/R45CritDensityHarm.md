VERDICT: INFO

Seat R45CritDensityHarm (leaf critic). Axis attacked: depth:density (SCORECARD axis 9) as measured by `corpus/instruments/density.py` over `SKILL.md`. Question: does appending a plausible 7-row Round-45 registry block lower or raise the mean, and does any block fall below `BAR_R15 = 142.5`? No lane file was edited; all fixtures lived in scratch (removed on exit). Only this Report was written.

## Pre-checks (base identity)

- `git -C <lane> show dc5bb8c6e31efc4a6650819df85e79b72fd64bcd:SKILL.md` is byte-identical to the working-tree `SKILL.md` (`cmp` printed nothing; `WT SKILL == base`). `git diff --quiet dc5bb8c6… HEAD -- SKILL.md` exits 0 ("SKILL.md unchanged dc5bb8c6..HEAD"). Freeze commit `8cf62c8` exists (`git cat-file -t` → `commit`).
- Base fixture: copy of `/fast/scratch/hyaku/kasegi-r45/L1/pure/SKILL.md` (`cmp` against lane file: "pure copy == WT SKILL").

## Finding 1 — base measurement (the do-nothing control)

Command: `python3 corpus/instruments/density.py SKILL.md --label r45base` (run from the scratch copy, exit 0). Quoted tail:

    | | **mean dens** | | | | | | | | **237.4** |
    Total path-citation instances: 793 across 31 blocks.

- A second identical run produced identical output (determinism, `diff` clean apart from the header).
- Blocks below `BAR_R15 = 142.5` at base (11 of 31): rows 1 (13.3), 2 (101.5), 5 (104.3), 7 (126.9), 9 (112.3), 10 (117.4), 11 (93.0), 13 (116.4), 15 (108.7), 16 (97.2), 17 (131.4 Triage economics).
- Attention: the frozen bar is a conjunctive rule (`corpus/instruments/README.md:69,79`: `BAR_R15 = 142.5`, conjunctive with ≥60 % path citations resolving). The base mean is now 237.4 over 31 blocks, not the 154.0 over 19 blocks recorded in `SCORECARD.md:65`/r25 rows. Re-computing the mean of the first 19 blocks of today's base output gives 158.1, so the recorded figure does not reproduce from the current file. I did not reconcile this (the mismatch is in the recorded history, not in this measurement).

## Finding 2 — the appended-block measurements

Variants (each = base bytes + one appended fragment; per-block rows 1–31 were diffed and are unchanged for the new-heading variants: `rows 1-31 identical (cites tbl num sig ev nb)`):

| variant | what was appended | new block row (ev, dens) | mean dens | Δ mean vs base |
|---|---|---|---|---|
| v5 blank-only (control) | one blank line | none | 237.4 | 0.0 (instrument ignores blank append) |
| v3 padded (control) | 7 rows with no digits/backticks | 10.0 | 230.3 | −7.1 |
| v4 heading-only (control) | `## Round-45 … registry addition` and nothing else | 100.0 (ev 1: the token `45` in "Round-45" counts as a numeric) | 233.1 | −4.3 |
| **v1b table (R3-compliant)** | 7-row 8-cell table, new `##` heading, appended at end | **430.0** (cites 28, tbl 7, num 7, sig 1, ev 43, nb 10) | **243.4** | **+6.0** |
| v7 table, path-only cites | same 7 rows, backticks only around bare script/file paths | **370.0** (cites 19, tbl 7, num 9, sig 2, ev 37, nb 10) | **241.6** | **+4.2** |
| v2 prose | same facts as prose, no table | 700.0 (cites 0, num 13) | 251.9 | +14.5 |
| v6 in-block | rows appended into existing block 31, no heading | block 31 333.3 → 400.0 | 239.6 | +2.2 |

Answer to the question: a table block raises the mean when its own density exceeds the current mean (237.4), and lowers it when it does not. The direction is set by the appended block's density, not by the table form. A 7-row table of real registrations clears `BAR_R15` (430.0 / 370.0 ≥ 142.5) and raises the mean; a 7-row padded table drops below the bar (10.0) and lowers the mean. Existing block values are not changed by a new-heading append (verified for v1). No block that was above the bar falls below it, and no block that was below it changes.

Form sensitivity (same facts): table 430.0 vs prose 700.0 (v1 vs v2); the prose variant scores higher only because bare numerals in prose count. Per the README's own warning (`corpus/instruments/README.md`, "density.py is form-sensitive"), a higher number from prose is not evidence and gets no credit.

## Finding 3 — the R3 counter predicate constrains the table shape (verifiability, not density)

`corpus/instruments/r45-routed-defects.py:194-206` (`limb_r3`) requires: append-only SKILL (`SKILL-not-append-only`), a `## Round-45 Gates & probes registry addition` section (`registry-section-absent`), and for each of `r44-frontier-count.py`, `r44-routed-defects.py`, `wave-registry.py` exactly one row with `len(rows[0].strip().strip("|").split("|")) == 8` (line 202). Running that exact split on the first draft:

    r44-frontier-count.py rows= 1 naive_cells= 8
    r44-routed-defects.py rows= 1 naive_cells= 10
    wave-registry.py rows= 1 naive_cells= 8

The draft's escaped pipes (`0\|1`) produced 10 naive cells → R3 would fail. Replacing `\|` with ` or ` gives `naive_cells= 8` for all three rows and leaves density unchanged (430.0 / 243.4, re-run). The recommended v7 block below has the same R3 shape (`naive_cells= 8` for all three rows, re-run on the v7 text).

## Finding 4 — citation resolvability (the second half of the conjunctive bar)

- `anchorcheck.py SKILL.md` on base and on v1 both print `SKILL.md: 16 in-range cite instances, 0 bad; 16 distinct anchors; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0` (exit 0). The appended block contains no `path:NN` anchors, so anchorcheck is neutral.
- `resolve.py` (instrument of record) on the **base** tree did not complete in this session: the background run ended with exit 143 and the census files were not rewritten (mtime equals the copy time), so no base census is claimed here.
- `resolve.py` on the **v1** tree completed (exit 0): `distinct=4140 resolves=40 mirror=0 internal=829 other=0 gone=3271 skill=94/655 corpus=836/3742 all=869/4140`. These totals are for the pure-export copy and are not comparable to the lane's committed census headline; I did not reconcile them. Per-citation classes for the 28 path-like cite instances in the v1 block (from `tree_v1/corpus/instruments/citation-survival.tsv`, matched by exact token):
    - INTERNAL 10 (includes 3 × `<tree>` that the glob classifier matched to `AGENTS.md` — a placeholder artifact, not a real resolution)
    - GONE 14 (every backticked command string such as `python3 corpus/instruments/r45-routed-defects.py --root <tree> --baseline <base>`, plus `corpus/source-snapshots/round-45/S071.txt` and `…/manifest.json`, absent at the frozen base)
    - NOT-IN-TSV 4 (`c2-gate fixed=<k>/7 exit=0 or 1`, `closed=<k>/8 …`, `dens = ev*100/nb`)
  Resolved fraction: 10/28 = 35.7 % (base tree); excluding the three `<tree>` artifacts, 7/28 = 25.0 %. This fails the ≥60 % gate.
- **Consequence for the table as drafted (v1b):** it clears the density half and fails the resolvability half. The failure is caused by form (command strings and `<placeholder>` tokens are counted as path citations), not by missing evidence.
- Path-only variant v7 (`block_v7` below): density 370.0 clears the bar. Its 19 cite instances are bare paths. Using the v1 census classes for the same bare paths (INTERNAL for every one that exists at base; the 5 round-45 cites GONE at base because the round-45 files are added by the freeze commit, not the base): **14/19 = 73.7 % at base; 19/19 expected at the lane head where the round-45 files exist** [INFERENCE from the v1 census classes; the v7 `resolve.py` run was started and cancelled on the L1's instruction, so it is not measured]. This passes the ≥60 % gate only by inference.

## Recommended block (v7, the form I recommend the L1 integrate; density 370.0, mean 241.6)

    ## Round-45 Gates & probes registry addition (appended 2026-10-28)

    | name | type | entry command | verdict map | self-test | pinned-value path | write scope | owner |
    |---|---|---|---|---|---|---|---|
    | r45-routed-defects.py | gate | `corpus/instruments/r45-routed-defects.py` with --root TREE --baseline BASE | one R1 to R5 line per limb, then routed-defects total=5 fixed=k exit 0 only for fixed=5 | `corpus/instruments/r45-routed-defects.py` --selftest, selftest cases=6 failures=0 | `corpus/lessons/round-44-verifier-spotcheck.md` section 6 | read-only over TREE | kasegi |
    | r45-c2-gate.py | gate | `corpus/instruments/r45-c2-gate.py` with --root TREE | one G1 to G7 line per limb, then c2-gate fixed=k/7 exit 0 only for fixed=7/7 | `corpus/instruments/r45-c2-gate.py` --selftest, selftest cases=7 failures=0 | `corpus/source-snapshots/round-45/S071.txt` | read-only over TREE | kasegi |
    | r44-frontier-count.py | gate | `corpus/instruments/r44-frontier-count.py` with --root TREE --expect 27 --ids | frontier rows=n admitted=k plus one id per counted row | `corpus/instruments/r44-frontier-count.py` --selftest, selftest cases=8 failures=0 | `corpus/README.md` Frontier table, third cell is status | read-only over TREE | kasegi |
    | r44-routed-defects.py | gate | `corpus/instruments/r44-routed-defects.py` with --root TREE | one D1 to D8 line per defect, then closed=k/8 exit 0 only for 8 | `corpus/instruments/r44-routed-defects.py` --selftest with --work DIR, selftest cases=12 failures=0 | `corpus/lessons/round-43-verifier-spotcheck.md` section 6 | read-only over TREE, scratch under --work | kasegi |
    | source-recheck.py | gate | `corpus/instruments/source-recheck.py` with --manifest PATH and optional --source ID | one OK or FAIL line per sha256 pin and quote assertion, exit 0 only when all hold | `corpus/instruments/source-recheck.py` --selftest, selftest cases=9 failures=0 | `corpus/source-snapshots/round-24/manifest.json` | read-only over the manifest directory | kasegi |
    | wave-registry.py | probe | `corpus/instruments/wave-registry.py` with --results FILE --out FILE --lane kasegi | writes seats=n and a populated names= field | none; re-read the emitted registry against the seat count | `.ufo/waves/round-43/w1-REGISTRY.txt` | writes only --out | kasegi |
    | density.py | probe | `corpus/instruments/density.py` SKILL.md --label X | per-block table and mean dens line, exit 0 | none; deterministic, re-run and diff | `corpus/instruments/density.py` docstring GENERIC_SIG list | read-only over the named file | kasegi |

Caveats on this block: the `selftest cases=` numbers (6, 7, 8, 12, 9) are the values the R3/R-counter contracts require or the L1 must confirm by running each `--selftest`; I did not run those selftests here. The R3 limb needs only the three 8-cell rows (r44-frontier-count.py, r44-routed-defects.py, wave-registry.py), which are present.

## Placement recommendation (harms no density axis)

1. **SKILL.md, new `##` block appended at the end** (this block). Reasons: the frozen R3 predicate (`r45-routed-defects.py:194-206`) reads exactly this section; `SKILL.md:1138` names SKILL.md as the registry home ("The registry home is this `SKILL.md` Gates & probes registry"). Density effect: existing blocks unchanged, mean 237.4 → 241.6 (v7) — a raise from a new dense block, which I record as no credit, not as a gain. No block that was above the bar falls below it.
2. **corpus/instruments/README.md: one row only** for `r44-frontier-count.py`, which R3 requires (`readme-row-absent`, `r45-routed-defects.py:205-206`). `density.py` reads only `SKILL.md`, so this edit moves no density number.
3. **Do not append rows into the Round-44 correction block** (v6). It changes block 31 from 333.3 to 400.0, breaks the new-heading structure R3 needs, and mixes a correction with registrations.
4. **Do not use a heading-only or padded block.** A bare heading scores 100.0 (the `45` in "Round-45"), and padded rows score 10.0; both are measurement artifacts, not evidence.

## Limitations

- `density.py` counts `<placeholder>` tokens and whole command strings as path citations (the `/` and `<` rules in `is_pathlike`), counts numerals in the heading ("Round-45" → 45), and is form-sensitive (table 430.0 vs prose 700.0 for the same content). The numbers above are the instrument's output, not evidence of the block's quality.
- The conjunctive gate's resolvability half was measured only for v1 (base tree + table) by reading the `citation-survival.tsv` classes. The base `resolve.py` run did not complete; the v7 `resolve.py` run was cancelled on the L1's instruction. The v7 resolvability (≥60 %) is therefore an inference from classes, not a measured pass.
- `resolve.py` took more than 300 s in the foreground and was not diagnosed (its glob/brace liveness on `<tree>`-style tokens is a suspect; not verified).
- The base mean 237.4 does not match the recorded 154.0 (SCORECARD r24/r25); not reconciled.
- Selftest counts quoted in the recommended block are the contract values, not re-run results.
- No live-target testing; documentation corpus only.

## Commands run (re-runs performed by this seat)

- `python3 corpus/instruments/density.py SKILL.md --label r45base` on the base copy → mean 237.4, 31 blocks, exit 0; second run identical.
- The same instrument on v1, v1b, v2, v3, v4, v5, v6, v7 copies → the mean and row values quoted above.
- `python3 corpus/instruments/anchorcheck.py SKILL.md` on base and v1 → `0 bad`, `LOST-RECORDED=306`, exit 0.
- `python3 corpus/instruments/resolve.py <tree_v1>` → exit 0 with the summary quoted in Finding 4.
- Inline checks (R3 naive split, per-block diffs, citation-class lookup) run in scratch only.
- No mutation of git/jj/index; no commit; scratch removed on exit.
