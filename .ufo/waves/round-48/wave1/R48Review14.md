# R48Review14 — Staged-source id collisions via 0-3-space parser (scratch derivation)

- **Seat:** R48Review14 (executor, leaf; no subagent dispatch, no production edits)
- **Round:** 48, wave 1 · **Lane:** kasegi-shokunin · **Axis:** depth:verifiability
- **Target claim:** C1 support context (canonical registry/census discipline around the SHONEN.md form repair; this seat derives staged-collision facts only, no checker claims)
- **Probe class:** positive/negative fixture derivation + read-only fleet census derivation — 0-3-space staged-id collision parser built and run in scratch
- **Date:** 2026-10-30

## Verdict

The 0-3-space staged-source id collision derivation **succeeds in scratch** and is **independently confirmed by the frozen tameshi `staged-id-guard.py` CLI**. The positive indented-S002 collision test fires as designed: a staged package row carrying `S002` indented by 2 spaces is extracted by the census-valid `^ {0,3}\|…` pattern, collides with the kasegi registry's `S002`, and is **missed by a column-zero parser** (`column0_miss: [S002]`) — i.e. a column-zero census would false-green the collision. No staged rows were appended anywhere; production registries were only read.

## Machinery built (scratch only)

- Scratch dir: `/fast/scratch/hyaku/kasegi-r48/R48Review14/` (created explicitly; receipts preserved here; dir removed on exit).
- `collide03.py` — independent 0-3-space extractor `ROW_RE = r'^ {0,3}\|\s*(S\d{3,})\s*\|'` plus column-zero control `COLUMN0_RE = r'^\|\s*(S\d{3,})\s*\|'`; emits one JSON object with per-side row counts, id lists, indented-row ids, collisions, `column0_collisions`, `column0_miss`, and SHA-256 of both input byte streams. Pattern basis: CORPUS.md "Maintained parser note" — the census CLI "accepts 0–3 leading ASCII spaces before Markdown table rows and headings; 4 or more spaces are indented code and are ignored", and CORPUS.md §Registry "id — S + 3 or more digits, the next unused; never reused."
- `sweep.py` — applies `collide03.py` to every sibling lane `corpus/SOURCES.md` treated as a staged package against the kasegi registry.
- `staged-package.md` — staged fixture (bytes quoted in §Positive test below).
- `kasegi-registry-copy.md` — byte-identical scratch copy of the production registry (sha256 match verified, see below).

Registry under test (read-only source): `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md`, sha256 `f0a3a3e96501545fb8457f303f005fa676830d844dea6b72b133ac49c280d613`, 77 ids `S001`–`S077`, **all column-zero** (production grep `^ {1,3}\| S[0-9]` count = 0; no 4+-space rows either). Copy sha256 identical.

No tool installs this seat (python3 3.14.8 stdlib only).

## Positive indented-S002 collision test

Fixture `staged-package.md` (sha256 `71474756dbf2e1ba8405422f28b37e3079cc4032cc2a6135119242b9da5d97d4`), full bytes:

```text
# Staged SOURCES package fixture — R48Review14 scratch (never appended anywhere)

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S101 | Staged Fixture Doc Alpha — https://example.invalid/alpha | docs | B | staged fixture scope alpha | fixture anchor A | staged teach alpha | mined | 2026-10-30 | 90d | — |
  | S002 | Staged Fixture Doc Beta — https://example.invalid/beta | docs | B | staged fixture scope beta | fixture anchor B | staged teach beta | mined | 2026-10-30 | 90d | — |
| S031 | Staged Fixture Doc Gamma — https://example.invalid/gamma | docs | B | staged fixture scope gamma | fixture anchor G | staged teach gamma | mined | 2026-10-30 | 90d | — |
    | S999 | Indented code, not a row — https://example.invalid/ignored | docs | B | staged fixture ignored | fixture anchor I | staged teach ignored | mined | 2026-10-30 | 90d | — |
| S102 | Staged Fixture Doc Delta — https://example.invalid/delta | docs | B | staged fixture scope delta | fixture anchor D | staged teach delta | mined | 2026-10-30 | 90d | — |
```

Row roles: `S101`/`S102` non-colliding staged ids; `S002` **2-space indented** colliding id (the positive test); `S031` column-zero colliding id; `S999` **4-space indented** — must be ignored as code. This mirrors the round-47 `R47ExecMergeGuard` precedent fixture (`  | S002 | fixture |`, 2-space indented).

**Observed — scratch parser:**

```text
$ python3 collide03.py --registry kasegi-registry-copy.md --staged staged-package.md
EXIT=0
```

Key receipt fields (`receipts/positive-indented-s002.json`):

```text
registry_sha256  f0a3a3e96501545fb8457f303f005fa676830d844dea6b72b133ac49c280d613
staged_sha256    71474756dbf2e1ba8405422f28b37e3079cc4032cc2a6135119242b9da5d97d4
extractor        0-3space
registry_rows_03 77
staged_rows_03   4
staged_rows_column0 3
staged_indented_ids [S002]
collisions       [S002, S031]
collision_count  2
column0_collisions [S031]
column0_miss     [S002]
```

The collision is **positive and indented-specific**: `S002` is a genuine registry id, the staged row is a genuine 0-3-space census row (2 spaces), and only the 0-3-space extractor sees it. `S999` at 4 spaces is correctly absent from both extractions (code, not a row).

## Frozen-guard cross-check

Frozen CLI (tameshi lane, executed read-only with `-I`):

```text
$ python3 -I /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/staged-id-guard.py \
    --registry kasegi-registry-copy.md --staged staged-package.md --json
EXIT=0
```

Guard verdict fields:

```text
verdict          answered
registry_rows    77
staged_rows      4
collisions       [S002, S031]
collision_count  2
column0_collisions [S031]
column0_miss     [S002]
extractor        0-3space
refused          False
unmapped         []
held             {}
next_free        S078
registry_max     S077
staged_max       S102
safe_floor       S103
registry_sha256  f0a3a3e96501545fb8457f303f005fa676830d844dea6b72b133ac49c280d613
staged_sha256    71474756dbf2e1ba8405422f28b37e3079cc4032cc2a6135119242b9da5d97d4
```

Byte-for-byte agreement with the scratch parser on staged/registry SHA-256s, staged row count, collision list, and the indented-row miss. Guard `--selftest` (CLI sanity, not a blanket verification): `STAGED_ID_GUARD_SELFTEST: cases=24 failed=0` / `VERDICT: PASS`, exit 0.

## Indent boundary matrix (S002 staged row at 0–4 leading spaces)

Five single-row fixtures, one run each:

```text
indent=0 staged03=1 column0=1 collisions=['S002'] column0_miss=[]
indent=1 staged03=1 column0=0 collisions=['S002'] column0_miss=['S002']
indent=2 staged03=1 column0=0 collisions=['S002'] column0_miss=['S002']
indent=3 staged03=1 column0=0 collisions=['S002'] column0_miss=['S002']
indent=4 staged03=0 column0=0 collisions=[]       column0_miss=[]
```

The 0-3-space census boundary holds exactly: the collision is detectable at 0–3 spaces (and only the 0-3-space extractor detects it at 1–3), and 4 spaces is ignored as code by construction. Receipts: `receipts/boundary-{0,1,2,3,4}.{md,json}`.

## Do-nothing control

```text
$ python3 collide03.py --registry kasegi-registry-copy.md --staged receipts/control-empty.md
staged_rows_03=0 collision_count=0   (empty staged package — no rows, no collisions)
```

No-output collision is the negative baseline: the positive finding above is attributable to the staged rows, not to parser noise.

## Fleet sweep — staged-source id collision landscape (read-only)

All 20 sibling lane registries were parsed with the same 0-3-space extractor and intersected with the kasegi id set. Per-lane receipts: `receipts/lane-<lane>.json`; summary: `receipts/fleet-sweep-summary.json`.

```text
lanes_scanned:            20
lanes_with_collisions:    20
total_collision_ids:      1318
```

| Lane | collision ids | Colliding set (head) |
|---|---:|---|
| audio-shokunin | 15 | S001–S015 (first 15 of registry range) |
| chousa-shokunin | 77 | S001–S077 (full overlap) |
| game-dev-2d-shokunin | 31 | S001–S031 … |
| game-dev-3d-shokunin | 36 | S001–S036 … |
| kagi-shokunin | 51 | S001–S051 … |
| kaidoku-shokunin | 77 | S001–S077 (full overlap) |
| kake-shokunin | 77 | full overlap |
| kama-shokunin | 77 | full overlap |
| kengaku-shokunin | 77 | full overlap |
| kotoba-shokunin | 77 | full overlap |
| kotodama-shokunin | 77 | full overlap |
| kumitate-shokunin | 77 | full overlap |
| lore-shokunin | 32 | S001–S032 … |
| mado-shokunin | 77 | full overlap |
| mori-shokunin | 77 | full overlap |
| revenger-shokunin | 77 | full overlap |
| souji-shokunin | 77 | full overlap |
| tabi-shokunin | 77 | full overlap |
| tameshi-shokunin | 75 | S001–S075 … |
| tsukuroi-shokunin | 77 | full overlap |

**Interpretation (no defect asserted):** every sibling numbers its own registry independently starting at S001, so cross-lane S-id overlap is the expected steady state, not an error; it is precisely why the guard's rule exists — a staged package built elsewhere keeps its own ids and cannot be appended as-is when its range overlaps the adopting registry. Notably, **no scanned sibling registry contains an indented (1–3 space) S-id row** (`indented_row_ids: []` in all 20 receipts), so the indented-collision hazard demonstrated by the positive fixture is currently latent in the fleet, not live.

**Frozen-guard corroboration on a real sibling** (kagi, the largest partial overlap):

```text
$ python3 -I …/tameshi-shokunin/tools/staged-id-guard.py --registry kasegi-registry-copy.md \
    --staged /home/vgpnk/Projects/shokunin/kagi-shokunin/corpus/SOURCES.md --json
EXIT=0  verdict=answered  collision_count=51
```

Exact list match with the scratch parser's `receipts/lane-kagi-shokunin.json` (51 ids, `match: True`).

## Expected vs observed

| Case | Expected | Observed | Match |
|---|---|---|---|
| Positive indented-S002 (2sp) | staged row extracted; S002 collides; column-0 misses it | `staged_rows_03=4`, `collisions=[S002,S031]`, `column0_miss=[S002]`, exit 0 | yes |
| 4-space `S999` row | ignored as code | absent from both extractions | yes |
| Frozen guard, same fixture | same collisions/miss, extractor `0-3space` | identical SHA-256s, `collisions=[S002,S031]`, `column0_miss=[S002]`, `verdict=answered`, exit 0 | yes |
| Boundary 0–4 spaces | detect 0–3, ignore 4 | matrix above matches exactly | yes |
| Do-nothing control | zero staged rows, zero collisions | `staged_rows_03=0`, `collision_count=0` | yes |
| Fleet sweep | lists/counts derivable read-only | 20/20 lanes collide; 1318 ids; receipts saved | yes |
| kagi corroboration | guard agrees with scratch parser | 51 = 51, exact list match | yes |

## Hygiene

- Wrote only this report plus scratch fixtures/receipts under `/fast/scratch/hyaku/kasegi-r48/R48Review14/`. **Staged rows were never appended** to the kasegi registry or any sibling registry; all registry reads were read-only, and the registry was exercised through a byte-identical scratch copy where a file path was needed.
- No production file, fleet file, sibling file, git/jj index or state, or `~/.local/bin` touched. No commit/push, no delegation, no background jobs, no tool installs (python3 3.14.8 stdlib only; tameshi guard executed read-only via its frozen CLI).
- Bounded probe only — the assigned derivation; no build/lint blanket verification (the guard's own `--selftest` and the two authorized counter executions above are the entire verification surface).
- Counter bytes/predicate frozen: the tameshi guard was executed, never amended; observed behavior reported verbatim.
- Scratch directory removed after this report was written; receipts quoted above preserve the evidence.

## Residual limits

- The positive test uses one staged shape (2-space indent); the boundary matrix covers 0–4, but tab-indented or mixed-whitespace staged rows were not exercised (tabs are not ASCII spaces under the CORPUS note).
- The fleet sweep counts id collisions only; it does not classify whether any colliding staged row is document-identical (the guard's `held` dedupe path) — that question is the guard's map flow, out of this seat's scope.
- The sweep is a point-in-time read of sibling registries as of 2026-10-30; registries are append-only but not frozen.
