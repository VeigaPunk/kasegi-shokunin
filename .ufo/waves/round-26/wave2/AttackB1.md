# AttackB1 — census exit re-measure (validate, conf lane id + explicit lane dir)

- Seat: L1Kasegi26.AttackB1 (leaf; no subagent dispatch).
- Date (UTC): 2026-10-25.
- Attacks: the claimed AFTER state "census exit 0; frontier-recheck-count …; no E09/E11 in kasegi SOURCES registry" — re-measured by re-running `scripts/sources-census.sh validate` and `census` against the lane.
- Verdict: PASS — exit 0 on every run; no E-codes; only the two pre-existing W04 warnings (S028/S029).

## Evidence

Tool: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` (unmodified, read-only run; no installs — nothing new installed, no channel used).

### Run 1 — conf lane id (the exact command in the assignment)

```
$ sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
EXIT=0
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
```

### Run 2 — explicit lane dir (with --root)

```
$ sources-census.sh validate --root /home/vgpnk/Projects/shokunin /home/vgpnk/Projects/shokunin/kasegi-shokunin
EXIT=0
kasegi-shokunin	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi-shokunin	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi-shokunin	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
```

### Run 3 — explicit lane dir (no --root, mirroring selftest `explicit-lane-dir` pattern)

```
$ sources-census.sh validate /home/vgpnk/Projects/shokunin/kasegi-shokunin
EXIT=0
kasegi-shokunin	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi-shokunin	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi-shokunin	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
```

### Code census (all three validate runs, programmatically counted)

- E-codes found: none (0 × E01–E12, including E09 and E11).
- W-codes found: exactly 2 × W04 per run (S028, S029); no other W.
- Lane status line: `ok` in every run.
- Exit: 0 in every run (validate exit 0 = clean or warnings-only; W04 is a warning, does not affect exit).

### Census re-measure (milestone)

```
$ sources-census.sh census --root /home/vgpnk/Projects/shokunin kasegi
EXIT=0
kasegi	rows	41
kasegi	tier.A	38
kasegi	tier.B	1
kasegi	tier.C	2
kasegi	status.mined	29
kasegi	status.queued	9
kasegi	status.rejected	3
FLEET	rows	41
FLEET	tier.A	38
FLEET	tier.B	1
FLEET	tier.C	2
FLEET	tier.invalid	0
FLEET	status.queued	9
FLEET	status.mined	29
FLEET	status.rejected	3
FLEET	status.invalid	0
FLEET	missing	0
```

Census exit 0, 41 rows (S001–S041), missing=0 — consistent with the integration-time measurement (census exit 0).

## Cross-checks against the registry

- W04 S028: expected. S028 (rejected, opened 2026-10-20) reuses the HackerOne safe-harbor URL already registered by S006, under a different scope ("Whether a new source row is needed to repair the r22 Gate's quote location" vs S006's safe-harbor scope). Same URL across scopes → W04 by design; rejected status exempts it from E04 (within-scope duplicate) and the W04 doesn't fail validation. Pre-existing.
- W04 S029: expected. S029 (mined, supersedes S024) reuses the EUR-Lex CRA URL of S024 under a different scope (Article 14/71 reporting clocks vs CRA purpose). Pre-existing.
- E09 (invalid recheck): none. Recheck cells are `NNd` (90d/180d/730d) or symbolic (`on-release`); S040/S041 cadence cells are bare `180d` in the registry (per `## Registry changes`), which the E09 regex accepts — no E09 fired.
- E11 (used-by path missing): none. All mined rows' used-by paths resolve under the lane dir; `usedby_findings` reported nothing.
- No E01–E08/E10/E12 either: lane is fully clean apart from the two W04s.

## Residual risk / verification gaps

- The validator checks used-by existence against the lane directory on disk (E11); it does not verify file content lineage — out of scope for this attack item.
- Explicit-dir runs label the lane by directory basename (`kasegi-shokunin`) rather than the conf id (`kasegi`); this is the script's documented resolver behavior (explicit dir → basename), not a defect, and both labels carry identical findings.
- No tools installed/updated this run (tooling directive record: none).
- No edits made to the lane; this report is the only output.
