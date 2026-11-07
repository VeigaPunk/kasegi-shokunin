# CriticHarm — round-95 harm audit (C1 `53ec479`, C2 `38e7319`; base `9ef0126`)

Seat: CriticHarm (leaf, no dispatch). Working dir `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Pins: base `9ef0126cc60b7f62baafd04f3e52c45e2a8e2f10`, freeze `347519f`, C1 `53ec479d71d25cf5be052db794a548a5904564b8`,
C2 `38e7319f44a9fab2978b59ffd43faf207cf62b32`, wave commit `d050e28`. The lane advanced under me during the audit to
`HEAD=43cc15e` (integration: LOG/SCORECARD/QUALITY/SOURCES/knowledge entry/lesson; none of the objects audited below);
governance blobs were re-checked at HEAD as well. Trees compared were `git archive <rev>` extracts in scratch; no
lane worktree or git state was mutated.

## Verdict

**NO HARM** on all four checks. Three routed defects, **none re-scores a frozen claim**.

## Item 1 — SKILL.md dense identity, PROVINCE/SHONEN/AGENTS untouched: **NO HARM**

- `SKILL.md` blob `27f23a93848be29b76992ac35ce423ab9a23c269` at base, C1, C2, `d050e28` and `HEAD` — identical; 1251 lines /
  156,631 bytes at both ends. Density census (`corpus/instruments/density.py`): mean dens **273.2**, **932** path-citation
  instances, 38 blocks, both sides — the density guard did not move because not a byte moved.
- `PROVINCE.md` `33458d01`, `SHONEN.md` `8c91054f`, `AGENTS.md` `29964529` — identical at all five revs.
- Non-`.ufo` path set of the whole round (base → `d050e28`) is exactly six files: the two `corpus/knowledge` files,
  `capture-secret-scan.py`, `capture-secret-allow.tsv`, `SCORECARD.md`, `corpus/source-snapshots/round-95/S142.txt`.
  No governance, manifest or fleet path was touched.

## Item 2 — untouched knowledge citation tokens, and resolution: **NO HARM**

- `corpus/knowledge/*.md`: 103 files at both revs, same set; **101 byte-identical**; the 2 changed files carry **14 changed
  lines** holding the 16 frozen rows (5 rows on the 5 iso lines; 11 rows on the 9 triage lines — L88 and L433 each carry two).
  Per-line token delta (resolve.py `is_pathlike` rule): the 12 removed token strings are exactly the mapped old forms
  (5 bare `S041.txt*` = GONE at base; 7 old labels `SKILL.md:10-11, 113-114, 175, 175-176, 245-247, 522` and
  `mission-control.md:21-23` = INTERNAL at base). No non-mapped token was removed or altered on any changed line
  (other path-like tokens kept per changed line: iso L13,34,43,54,64 = 1,0,0,0,1; triage L88,89,90,356,396,433,434,435,436
  = 0,1,2,0,4,0,1,0,3 — every one byte-identical before and after).
- `corpus/instruments/resolve.py` count over its own scope, re-derived here (collect + classify, per-token 5 s bound):
  **base 1007/1998 → C1 1008/1994** (INTERNAL 984→985, RESOLVES 23→23, GONE 991→986) — matches the frozen meter M0/M1
  independently. Shared tokens 1986, **class changes 0**, **resolved→GONE 0**. Removed 12 / added 8 (all 8 added resolve).
- Full scope (`SKILL.md` + `corpus/**/*.md`): base distinct 7778, occurrences 15998, files-with-citations 324,
  GONE 5206 → C1 distinct 7775, occurrences 15999, files 324, GONE 5202; shared 7767, **class changes 0**,
  **resolved→GONE 0**. Nothing that resolved at base stops resolving at the landing.

## Item 3 — the C2 scanner cannot mask an earlier shape: **NO HARM**

- Sample: **200 plants / 24 families** built in scratch (real-shape plants for every pre-existing class, new-shape plants
  for `ghr_`+76 and `glcbt-`/`glsat-`/`gliamat-` JWT, plus near misses `ghr_`+75, `ghr_`+77, malformed `glcbt-`).
  Round-94 scanner (base `9ef0126`) vs landed scanner (C2), same files, same allow handling:
  150 (path, shape) pairs → 195 pairs; **base-only 0**, tip-only 45 = 10 `github-refresh-token` (the `ghr_`+76 plants)
  + 35 `gitlab-jwt-token` (glcbt/glsat/gliamat/custom-prefix plants). Near-miss plants hit on neither side.
  Per-shape totals for every old class are identical (github-token 40, gitlab-pat 10, gitlab-runner 10, gitlab-deploy 10,
  aws 10/10, cloud 10/10/10/10, gate shapes 3/3/10/4).
- Static corroboration: the instrument diff C1→C2 is **23 insertions, 0 deletions** (`git diff --numstat`) — every earlier
  regex byte is preserved; the base instrument contains 0 occurrences of either new shape name, the landed one 8.
- Same test on committed trees: `--rev 9ef0126` with the round-94 scanner → `hits=0 allowed=24`; `--rev 38e7319` with the
  landed scanner and landed allowlist → `hits=0 allowed=26`; both rc 0.

## Item 4 — the allowlist row allows only that one digest: **NO HARM**

- Net allowlist delta: **+1 row** (23 → 24); key is `(path, shape, sha256-of-matched-bytes)` and the new row is
  `github-refresh-token` (not in `NEVER_ALLOWED`). Independent digest of the two matched byte-strings in that receipt:
  `c7ad99a1ba7ef9a9eb954d3b93e3dea3d109ac298fc2c580cacf35c959ef060d` (= the row's digest; 2 matches, 1 distinct digest).
- Binding tests at the same shape: same path + **one byte changed** → `HIT shape=github-refresh-token ... line=10`, rc 1;
  same value at **another receipt path** → `HIT`, rc 1; exact path + exact value → `hits=0 allowed=2`, rc 0.
  So the row is both value-bound and path-bound; it cannot allow a different token, nor the same token elsewhere.

## Routed defects (none changes a verdict)

**D1 — the landed scanner documents a false limit (doc/code contradiction).** At C2 and still at HEAD,
`corpus/instruments/capture-secret-scan.py` "Known limits" lists "the JWT-form GitLab tokens (`glcbt-eyJ…`, `glsat-eyJ…`,
`gliamat-eyJ…`; S140 lines 430, 447, 464)" as *undetected* — the exact class the landing now detects — and the "Shapes."
block has **0** entries for `github-refresh-token` or `gitlab-jwt-token` (the `ghr_`+76 bound is explained nowhere outside
a code comment). A reader of a security instrument is told a hole exists where there is none. That the JWT boundary and the
`gliamat-` no-prefix form match S140 lines 429/446/463 exactly (verified against the snapshot) is fine; the defect is
documentation. **Does not re-score C2** (P1–P3 read capability-check output, the two sha256 pins and the commit path set;
none reads the docstring). Smallest safe correction: move the three JWT forms out of "Known limits" into the "Shapes." block
and add one entry per new shape citing S142 L169 / S141(S143) L72 / S140 429,446,463.

**D2 — one bare `S041.txt` capture citation survives the tranche.** In `iso-29147-divergence-and-clause-crosswalk.md`
line 13 the backticked `` `S041.txt:1680-1681` `` is still GONE at the landing (3 GONE tokens remain in that file: this
cite, a shell command string, and the staged-entry filename). It is the same class tranche 10 closed, but it is not one of
the frozen five. **Does not re-score C1** (the statement names five, and all five converted) — routed as the next tranche's
row, not as a regression: GONE count for the file fell 8→3 and no token regressed.

**D3 — the census of record is stale (pre-existing), and the landing adds drift.** `corpus/instruments/citation-survival.tsv`
at C2 still carries rows for tokens the landing removed (`S041.txt:1868-1870` GONE, `SKILL.md:522` INTERNAL) and has rows
for only 1 of the 8 added tokens (the plain `corpus/source-snapshots/round-30/S041.txt`, already cited by
`japanese-severity-vocabulary-and-impact-model.md`); it reads 5152 distinct / 10931 occurrences / 224 citation-bearing files
while the same instrument reads **7778 / 15998 / 324 at base already**. So `census-freshness-check.py` is stale at base too:
round 95 does not turn a green gate red, it adds 2 stale rows and 7 missing rows. **Does not re-score C1 or C2** (neither
predicate reads the census pair; the meter is the C1 counter of record). Recorded so the drift is not mistaken for a
round-95 regression. The gate itself was not executed against the lane (it writes and restores the two census files).

## Notes (not defects)

- S141's 76-character bound is grounded: `S141` (registry row at `corpus/SOURCES.md:153`) is tier B / rejected, and its
  line 72 (`72:regex = "ghr_[0-9a-zA-Z]{76}"`) is held in `.ufo/waves/round-94/w1/ScoutGitLabRules-receipts/08-github-rules-file.txt`
  with raw digest `02c67ceb…`, 130 lines / 3955 bytes; the integration commit `43cc15e` adds S143 superseding S141 with
  used-by naming the scanner, so the registry breadcrumb exists at HEAD (outside the audited pins).
- `resolve.py`'s CLI cannot finish on this host in reasonable time because one token (`~/Projects/**`) recursive-globs the
  whole `~/Projects` tree (>6 min at base, >8 min at C1; both runs stopped). Counts above therefore come from resolve.py's
  own `collect()`/`classify()` with a 5 s per-token bound; exactly that one token timed out at both revs, identically.
  Pre-existing instrument behaviour, unrelated to round 95.

## Axes

`depth:verifiability` (item 2) and `coverage` (items 3/4): no movement claimed by this seat and none implied — a harm audit
can only refuse a movement, and nothing here refuses one. D1–D3 are routed, not scored.

## Receipts

Directory: `.ufo/waves/round-95/w1/CriticHarm-receipts/`.

| # | Command (abridged) | Observed |
|---|---|---|
| `01-governance.txt` | `git rev-parse <rev>:SKILL.md PROVINCE.md SHONEN.md AGENTS.md` for base/C1/C2/d050e28/HEAD | 4× IDENTICAL; `density.py` mean dens 273.2 / 932 instances both sides; `wc -c -l` 1251 / 156631 both sides |
| `02-knowledge-identity.txt` | token/byte identity check over `corpus/knowledge/*.md`, base vs C1, resolve.py `is_pathlike` | `knowledge_md base=103 c1=103 same_set=True`, `byte_identical=101 changed=2`, 14 changed lines, 12 removed/8 added tokens listed |
| `03-citation-counts-knowledge.txt` | resolve.py `collect`+`classify`, `corpus/knowledge` scope | base 1007/1998, C1 1008/1994; shared 1986, class_changed 0; removed 12 (5 GONE + 7 INTERNAL), added 8 (all INTERNAL); `no_token_lost_resolution=True` |
| `04-citation-counts-full.txt` | same, full scope (SKILL.md + `corpus/**/*.md`) | base 7778 tokens / 324 files / GONE 5206; C1 7775 / 324 / GONE 5202; shared 7767, gone→resolved 0, resolved→gone 0, other class changes 0; 1 token `~/Projects/**` timed out at both revs |
| `05-plants-masking.txt` | `--files r95-receipts/*.txt` with both scanners; `comm` of (path, shape) sets | base `hits=150 files=140`, landed `hits=195 files=185`; base_pairs 150, tip_pairs 195, **base_only 0**, tip_only 45 (10 github-refresh-token, 35 gitlab-jwt-token) |
| `06-allowlist.txt` | allow diff, independent sha256 of matched bytes, three binding tests | 23→24 rows; digest `c7ad99a1…` = row digest (2 matches / 1 digest); mutated value rc 1 HIT, other path rc 1 HIT, exact rc 0 `allowed=2` |
| `07-selftest-and-diff.txt` | `--selftest` both revs; `sha256sum`; `git diff --numstat` C1→C2 | base `cases=101`, landed `cases=115`; instrument `66edd661…` = pin, gate `8b6f8493…` = pin; scanner 23/0, allow 1/0, SCORECARD 1/1 |
| `08-rev-scans.txt` | `--rev` scans of the committed trees | base rev `scanned=2476 hits=0 allowed=24 rc=0`; C2 rev `scanned=2477 hits=0 allowed=26 rc=0` |
| `09-residual-stale.txt` | residual `` `S041.txt:1680-1681` ``; census rows; census headline vs regenerated; docstring limits | 1 residual bare cite; removed-row/absent-row evidence; 224 files / 5152 distinct vs 324 / 7778; "Known limits" JWT line present, 0 Shapes entries |
| `10-landing-paths.txt` | `git diff --stat` C1, C2; non-`.ufo` path sets; CLI stall note | C1 2 files 14/14; C2 3 files 25/1; round 6 non-`.ufo` paths; `~/Projects/**` stall |
| `11-shape-source.txt` | S142 L169, S140 429/446/463, landed regex block | prefix "starts with ghr_" (no length); glcbt/glsat carry `(?:[a-zA-Z0-9]{1,20}-)?`, gliamat does not — code matches source |
