# ExecC1Hunt — next repairable citations beyond the frozen 18 (round 86)

Seat: ExecC1Hunt (leaf). **Nothing edited in the lane tree except the two outputs below.**
Frozen round-85 C1 target (158/741 → 167/732) is **unchanged**; everything here is a routed candidate for round 86.

Files written:
- `.ufo/waves/round-85/w1/ExecC1Hunt.md` (this report)
- `.ufo/waves/round-85/w1/ExecC1Hunt-r86-candidates.json` (JSON candidate map)
- `.ufo/waves/round-85/w1/ExecC1Hunt-receipts/` (hunt scripts + outputs)

## Method

All classification used the frozen instrument itself — `corpus/instruments/resolve.py`
imported with `sys.path` (per the spec: `collect()` over a scratch dir holding only
SKILL.md, `classify()` against `/home/vgpnk/Projects/shokunin/kasegi-shokunin`),
never a re-implementation. Base revision `bc722e5` (freeze base), landed revision
`c0507ad` (round-85 C1 landing, which `git log` shows already applied the frozen 18).
No full census was run (per the spec's ~6 min / 13 GB warning — actually untouched,
since the skill-meter scope is exactly the census of concern).

Ground truth re-verified with the frozen counter's own semantics at both revisions:
- base `SKILL.md`: **741 tokens, 583 GONE, 158 non-GONE** (matches the frozen base 158/741)
- landed `SKILL.md`: **732 tokens, 565 GONE, 167 non-GONE** (matches the frozen target 167/732)
- all 18 frozen map values classify `INTERNAL` and are git-tracked at base; all 18 keys GONE at base.

Rules tried (one candidate per GONE token at most, first hit wins): **B** = first
space-separated word of a command-invocation token that exists verbatim as a lane
file (the token names the script being invoked, e.g. `python3 corpus/instruments/x.py --selftest`);
**C** = `[lost-*]` inner path exists literally; **D** = `corpus/` + token exists;
**F** = brace expansion has exactly one existing member; **G** = `corpus/knowledge/` + token exists;
**H** = `[lost-*]` inner path's historic blob is byte-identical (sha256) to a same-basename
fixture/snapshot file; **I** = one same-stem tracked sibling in an existing directory.
Rules C, D, F, G, H, I produced **zero** candidates; only B produced candidates.
Each candidate was then re-verified against the **landed** SKILL.md: token still GONE,
proposed value classifies `INTERNAL`, and the value is not already a distinct cited
token at landing (a rewrite whose value is already cited would only ever act as a
de-cite — the round-85 do-nothing forgery `158/723`).

## Candidates for round 86 (31 tokens → 19 distinct files)

Every candidate is rule **B** (invocation tokens whose first existing word is the
instrument). If *all 31* were applied, the SKILL meter would move **167/732 → 186/701**
(each distinct new cited value adds 1 to the numerator; each removed GONE distinct
token subtracts 1 from the denominator; 12 of the 31 collapse onto a value already
invoked by a sibling token). Full token/line/context table is in the JSON map
(`skill_candidates`, with `base_lines` and `landed_lines`).

| Tokens | Proposed path | Rule | Why this file |
|---|---|---|---|
| `bash corpus/instruments/r35-defect-closure.sh --selftest`, `… [--root DIR]` | `corpus/instruments/r35-defect-closure.sh` | B | entry-command column for the r35 gate; only that .sh exists |
| `bash corpus/instruments/r36-closure.sh --export-ref <hash>`, `… --selftest` | `corpus/instruments/r36-closure.sh` | B | entry-command column for the r36 gate |
| `bash corpus/instruments/r37-closure.sh --export-ref <hash>`, `… --selftest` | `corpus/instruments/r37-closure.sh` | B | r37 gate entry command |
| `bash corpus/instruments/r38-closure.sh --export-ref <hash>`, `… --selftest [--export-ref <hash>]` | `corpus/instruments/r38-closure.sh` | B | r38 gate entry command |
| `bash corpus/instruments/r39-closure.sh --export-ref <hash>`, `… --selftest --export-ref <hash>` | `corpus/instruments/r39-closure.sh` | B | r39 gate entry command |
| `bash corpus/instruments/r40-closure.sh --export-ref <hash> […]`, `… --selftest` | `corpus/instruments/r40-closure.sh` | B | r40 gate entry command |
| r41 pair | `corpus/instruments/r41-closure.sh` | B | r41 gate entry command |
| r42 pair | `corpus/instruments/r42-closure.sh` | B | r42 gate entry command |
| r43 pair | `corpus/instruments/r43-closure.sh` | B | r43 gate entry command |
| `bash corpus/instruments/r46-plain-measure.sh TREE` | `corpus/instruments/r46-plain-measure.sh` | B | the counter named by the r46-plain-measure row |
| `python3 corpus/instruments/r47-routed-defects.py --root TREE` | `corpus/instruments/r47-routed-defects.py` | B | frozen-diagnostic entry command |
| `python3 corpus/instruments/r47-f30-gate.py --root TREE` | `corpus/instruments/r47-f30-gate.py` | B | frozen-diagnostic entry command |
| `python3 corpus/instruments/r47-counters-selftest.py --base … --counter both` | `corpus/instruments/r47-counters-selftest.py` | B | gate entry command |
| `python3 corpus/instruments/r47-mutbat.py --base … --counter both` | `corpus/instruments/r47-mutbat.py` | B | gate entry command |
| `python3 corpus/instruments/shonen-form-selftest.py --root TREE --work SCRATCH` | `corpus/instruments/shonen-form-selftest.py` | B | self-test runner named in the shonen-form row |
| `python3 corpus/instruments/shonen-shipped-fixture-check.py --root TREE` (+ `--work SCRATCH` form) | `corpus/instruments/shonen-shipped-fixture-check.py` | B | probe entry command |
| `python3 corpus/instruments/citation-ground-check.py --root TREE …`, `… --selftest` | `corpus/instruments/citation-ground-check.py` | B | gate entry commands |
| `python3 corpus/instruments/figure-audit.py --selftest`, `… [--ledger PATH] [--root DIR]` | `corpus/instruments/figure-audit.py` | B | the two entry commands in the figure-audit registry row (reg. round-58, QUALITY R29 exact basenames; file tracked since round-72) |
| `python3 corpus/instruments/figure-audit-mutbat.py` | `corpus/instruments/figure-audit-mutbat.py` | B | mutant-battery entry command in the same row |

Excluded under rule B (13 tokens, listed in the JSON as `excluded_ruleB` with the
reason): their proposed value is **already a distinct cited token at landing**
(e.g. `bash corpus/instruments/r-defect-closure.sh --selftest` → `r-defect-closure.sh`
is already cited 1+ times), so rewriting them is numerator-neutral (a pure de-cite,
denominator −1, numerator unchanged) — the exact shape of the round-85
`158/723` do-nothing forgery. One more (`python3 corpus/instruments/` → a *directory*)
is excluded because the value is not a tracked file (M4 binding requires a file).

## Rules that produced nothing (measured, not assumed)

- **C (lost-marker literal unwrap):** zero of ~250 `[lost-base]`/`[lost-tree]` tokens
  exists literally in the lane. Sample spot checks: every `ops/*.mjs`, `docs/*`,
  `fleets/*`, `claims/*/*`, `evidence/*` inner path names the absent bounty roots
  (`~/Projects/bounties`, `~/Projects/the-bounty-hunter`) — they are history, correctly
  recorded as lost, and have no lane counterpart.
- **H (byte-identical):** zero candidates measured. The check is exact sha256 of the
  historic blob vs every same-basename tracked file under `corpus/source-snapshots/`
  or `corpus/instruments/fixtures/`, over all 10,949 paths ever in lane history. The
  nearest misses are the claim-package contract names (`report.md`, `status.json`,
  `manifest.json`, …), which are *rule E* below, not byte-identical repairs:
  `claim_checklist.md` is byte-identical across all 18 fixture copies (it is a
  contract name, identical by construction), and `status.json` has 5 distinct hashes
  among 20 fixture copies — no unique winner.
- **D/G (missing `corpus/` or `corpus/knowledge/` prefix):** zero. Including the
  tempting `report.md`/`status.json`/`provenance.json`/`claim_checklist.md`/
  `custodian-receipts.json`/`evidence/manifest.json` contract names, and every
  `S###.txt` basename in SKILL.md (all snapshot citations in SKILL are already full
  `corpus/source-snapshots/…` paths; the bare `S040-live.txt`/`S073.txt`/`S074.txt`
  were the frozen 18).
- **F (brace single-hit):** zero in SKILL.md. All brace/glob tokens (e.g.
  `~/Projects/bounties/ops/{…}.mjs`) are bounty-root domain tokens classified GONE
  by the absent root; none has a lane-side expansion.
- **I (same-stem rename):** zero. Every GONE relative token names its directory's
  tracked file set or none (the stray stems-lemmatised `fleets/registry.json`,
  `submit/receipt.md` have no same-stem sibling — the hits were unrelated files).

## Ambiguous basenames (10) — context picks nothing unique

`report.md`, `status.json`, `provenance.json`, `claim_checklist.md`,
`custodian-receipts.json`, `evidence/manifest.json`, and full claim-tree paths
`claims/bugcrowd-seek/honest-zero/evidence/status.json`,
`claims/cantina-pendle/ingestion-20260915/status.json`, `claims/immunefi-beanstalk/…/provenance.json`,
`claims/cantina-pendle/…/provenance.json` match **9–70 tracked fixture/bounty-tree
files each**, and the SKILL contexts are generic contract census counts ("280
packages' `status.json`", a column describing the six-file *shape*), not pointers to
any one fixture copy. Pointing any of them at one fixture copy would be a *wrong-target*
forgery of the round-85 kind — no candidate proposed, deliberately. Reclassified as
topic names; a round-86 repair could only apply if the surrounding row named a
specific defect fixture (none does).

## Corpus/knowledge census (the same unique-basename class, counted)

Spec glob `corpus/knowledge/*.md` (top level only; lessons are not under
`corpus/knowledge/`): **98 files, 1,721 distinct tokens, 1,322 GONE, 399 non-GONE,
496 distinct tokens resolve by the frozen unique-basename rule (764 total
occurrences)** — vs 18 in SKILL.md. Plus the same three tokens recur with frozen-18
values (`resolve.py`, `capture-source.py`, `source-recheck.py`). By proposed directory:
`corpus/knowledge` 110, `corpus/source-snapshots/round-68` 70, `round-40` 42,
`round-69` 40, `round-45` 39, `round-70` 36, `round-47` 32 — the bulk is `S###.txt`
snapshot citations and `considerthese/2026-10-*.md` with `:line` anchors, and the
top-level `*.md` knowledge files. (`corpus/knowledge/**/*.md` is the same 98 files —
no nested .md beyond the top level.) A knowledge-scope round could move that
sub-meter by 399 → 895/1,721 if all 496 were applied, but that is a *different*
scored-meter scope than the round-85 SKILL claim; recorded here as measured exposure,
not as an entry in the round-86 SKILL map.

## Caveats

- Candidates are counted at the **landed** commit; the L1 should re-derive them at
  the round-86 base (any commit between landing and base that touches the same rows
  invalidates the per-token lines).
- Two different rule-B rewrites onto the *same* value on the *same line* would
  collapse that line's distinct citations; none of the 31 shares a line with another
  candidate whose value is identical except where recorded, and no value is already
  cited — but the level of the 186/701 figure assumes all 31 are applied together.
- The 10 ambiguous tokens stay GONE by measurement; any future rule that *would*
  pick one must name the fixture in surrounding prose, which SKILL.md does not.

Scratch (per the 2026-10-25 directive) was `/fast/scratch/hyaku/kasegi-r85/ExecC1Hunt/`
and was removed (`rm -rf`) after copying receipts. No tools were installed; all runs
used `python3 -B` (no `__pycache__` writes).

Report: `.ufo/waves/round-85/w1/ExecC1Hunt.md`
