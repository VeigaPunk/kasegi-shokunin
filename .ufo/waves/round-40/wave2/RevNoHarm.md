# RevNoHarm — attack the no-harm guard (H10) at the round-40 verification ref

Seat: `RevNoHarm` (leaf reviewer, round 40, falsify wave 2, dispatched by L1 KasegiR40 via
inline spawn handoff, hyaku run 9).
Item: attack the no-harm guard — at Y vs base `a7af2ce63bce153757d39bf66b366a96caf30c13`,
confirm every changed path is N/0 (additions only), `SKILL.md` and `PROVINCE.md` are
append-only, `sha256sum corpus/instruments/density.py` is unchanged, and
`python3 corpus/instruments/density.py SKILL.md --label SKILL` + `anchorcheck.py SKILL.md`
behave as recorded. Any deletion, mid-file edit of a cited file, or instrument change is a
defect.

- Deliverable: `.ufo/waves/round-40/wave2/RevNoHarm.txt` (byte-exact outputs fixture)
- Lines: **134** — Bytes: **7531**
- sha256: `dc7014469859b075bb47c43c92d1d11f671bf774454e5b87efbf5be59641c990`
- Run UTC: 2026-10-26T22:0x–22:1xZ (all reads after this seat's spawn; nothing back-dated).
- Lane mutations: **none**. Every git invocation was `rev-parse`, `cat-file`, `show`,
  `diff`, `archive`, `log`, `status` — read-only. Instruments were run inside `git archive`
  exports under scratch and once in the lane working tree (stdout-only, no writes).
- Tooling: no installs, no upgrades (nothing was needed; `python3`, `git`, `awk`, `cmp`
  sufficed).
- Disk guard: `bash scripts/hyaku/disk-guard.sh status` run before the heavy pass
  (/fast/scratch/hyaku at 24%, 615.4G free).

## 0. What "Y" is at attack time (verification-scope note)

The frozen claims define Y = judged head J + the receipt
`.ufo/waves/round-40/final-gates/all-gates.txt` only. At attack time **no commit in the
repository contains that path** (`git log --all --oneline -- .ufo/waves/round-40/final-gates/`
prints nothing): the receipt is an **untracked** file at the lane tip, and the lane tip HEAD
is `3074c7679d6f527ec3930d7748ccce1dbae4a58a` (= J5, the commit the receipt itself names as
`export-ref`). So Y is not yet a commit; the integrated lane state is J5 plus the untracked
receipt. Because this seat's pathspec (`-- . ':!.ufo'`) excludes `.ufo`, and Y's only delta
vs J5 is that one `.ufo` receipt path, `git diff --numstat <base> <Y> -- . ':!.ufo'` is
byte-identical to the base→J5 diff actually run below. Gap: the claims' `git diff
--name-only J Y` = `all-gates.txt` equality is not testable until Y is committed.

## 1. Axes and the move

Axes owned by the host claims: `depth:verifiability` (C1), `coverage` (C2), with
`depth:verifiability` also this seat's judged axis. One move, four limbs, each run against
the committed bytes (blobs read via `git show`, never the working tree alone), with the
stronger test applied wherever the committed guard is weaker than this seat's criterion:
byte-prefix append-only (guard only asserts deleted==0) and instrument re-execution (guard
only digests density.py).

## 2. Runs and results (full outputs in RevNoHarm.txt)

### Limb 1 — numstat additions-only: 28/29 paths PASS, 1 CONTRADICTED (classified)

`git diff --numstat a7af2ce6… 3074c76… -- . ':!.ufo'` → 29 paths, 6475 added, **9 deleted**.
Every path is N/0 except:

```
12	9	corpus/SOURCES.md
```

Field-level classification of all 9 deleted lines (each paired with its replacement row):

| row | fields changed |
|---|---|
| S016 | col8 `queued`→`mined`; col11 `—`→`corpus/knowledge/anthropic-cvd-provenance-and-pacing.md` |
| S017 | col8 `queued`→`mined`; col11 `—`→`corpus/knowledge/pz-reporting-transparency-trial.md` |
| S019 | col8 `queued`→`mined`; col11 `—`→`corpus/knowledge/nist-sp800-216-vdp-framework.md` |
| S020 | col8 `queued`→`mined`; col11 `—`→`corpus/knowledge/doj-vdp-framework-scope-and-authorization.md` |
| S021 | col8 `queued`→`mined`; col11 `—`→`corpus/knowledge/cisa-bod-20-01-vdp-minimums.md` |
| S022 | col8 `queued`→`rejected` (only) |
| S023 | col8 `queued`→`mined`; col11 `—`→`corpus/knowledge/cisa-cvd-program-stages.md` |
| S024 | col8 `queued`→`rejected` (only) |
| S025 | col8 `queued`→`mined`; col11 `—`→`corpus/knowledge/cve-bench-agent-exploitation-benchmark.md` |

Every URL, title, class and every other field is byte-identical across each rewrite; the
only changed fields are the status and the entry pointer — exactly the fields C2's frozen
predicate promises to change ("each is `mined` … or `rejected`"). The 12th added line-group
is 3 new rows S060/S061/S062 inserted immediately after the previous last registry row S059
(base line 65 → J5 lines 66–68), before the unchanged `## Paths` section — the C2-promised
"S060+ opened this round". No line of SOURCES.md was destroyed: 9 rewrites carry all prior
content forward.

**Finding F1 (the one disagreement, reported as required):** the seat's literal
"every changed path is N/0" criterion is **contradicted** by `corpus/SOURCES.md` (12/9).
Substantively this is the C2 deliverable operating as the frozen claims promise — a row
status flip is an in-place edit by construction — and the committed H10 guard deliberately
does not assert N/0 for SOURCES.md (the wave-1 baseline receipt `ExecH10NoHarmBase.md` §5
R4 states no-harm "does not cover corpus/SOURCES.md … growth is allowed, deletion anywhere
is not", i.e. deleted *paths*). Recommendation: judge F1 against the guard's contract, not
the seat's shorthand; no content was lost. If the L1 wants the letter of N/0 enforced, the
guard and the seat criterion need reconciling — that is a spec tension, not round-40 harm.

Also verified: `--diff-filter=D` whole-tree count = **0**; `--diff-filter=R` = **0** (the
guard's DR limb passes); `--name-status` shows only `M`/`A`, no `D`/`R`/`T`.

### Limb 2 — SKILL.md and PROVINCE.md append-only: PASS (byte-prefix, stronger than guard)

Byte-prefix test (base blob is a prefix of the J5 blob, insertion at EOF only):

| path | base | J5 | first-diff byte | append-only |
|---|---:|---:|---:|---|
| `SKILL.md` | 112245 B | 113282 B | 112245 (= base EOF) | **TRUE** |
| `PROVINCE.md` | 12057 B | 12382 B | 12057 (= base EOF) | **TRUE** |

Guard limb `git diff --numstat <base> <J5> -- SKILL.md PROVINCE.md` → `7 0` and `3 0`.
Base digests match the recorded baseline exactly (`h10.skill.base.sha256` =
`ce6689c554f2e33b…`, `h10.province.base.sha256` = `4d42eed1afa00ff0…`). What was appended:
SKILL.md +7 lines (the "Round-40 Gates & probes registry addition" block, one r40-closure.sh
row); PROVINCE.md +3 lines (the F23 frontier amendment). No mid-file edit of either cited
file — the byte-prefix proof is strictly stronger than the guard's deleted==0 assertion,
which a mid-file pure insertion would slip past.

The other 8 modified paths are all byte-prefix append-only too: `LOG.md`, `SCORECARD.md`,
`SHONEN.md`, `corpus/QUALITY.md`, `corpus/README.md`, `corpus/lessons/round-39.md` (all
TRUE). The two non-append-only paths are `corpus/SOURCES.md` (F1 above) and
`corpus/instruments/knowledge-expected.txt` — N/0 (8 added, 0 deleted), 8 sorted-position
insertions required by the fixture's own contract ("Sorted list … keep in sync with
corpus/knowledge/"); it is an expected-values fixture for `recheck-audit.py`, not an
instrument, and no line was deleted.

### Limb 3 — density.py unchanged: PASS

`sha256(corpus/instruments/density.py)` = `ee803726a3229eb924a6798fe0cf5309dacd33d42c40568da55d5c95f9f54710`
at base, at freeze `5e985b74`, at J5, **and** in the working tree on disk — identical to the
recorded `h10.guard.expect-density-sha256` and to the `DENSITY_SHA=` pin inside the
committed `r40-closure.sh` (line 167). Bonus: `anchorcheck.py` is likewise unchanged
(`d0f35f8ccdcf995b78ea1403732fa90e12708b79bda21793002f7315b0e2a912` at all three refs). The
only instrument-subtree change is the round-40 **addition** `corpus/instruments/r40-closure.sh`
(new file, expected per ExecH10NoHarmBase §5 R2) plus the `knowledge-expected.txt` fixture
growth above. No instrument was modified.

### Limb 4 — instruments behave as recorded: PASS (byte-exact at freeze, clean at J5)

Re-runs inside `git archive` exports under scratch (export-mode parity, as the suite runs):

At freeze `5e985b74` — **byte-matches every recorded reading** in
`wave1/ExecH10NoHarmBase.txt`:

```
# Density census — SKILL (1115 lines, 27 blocks)        (recorded: 1115 / 27)
| | **mean dens** | | | | | | | | **232.9** |            (recorded: 232.9)
Total path-citation instances: 771 across 27 blocks.     (recorded: 771)
== SKILL.md: 16 in-range cite instances, 0 bad; 16 distinct anchors; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0
                                                          (recorded: 16/0/16/306, all guard fields 0)
```

At J5 `3074c76` — clean runs, rc=0 both:

```
# Density census — SKILL (1122 lines, 28 blocks)         (+7 lines = the appended block)
| 28 | Round-40 Gates & probes registry addition … | 250.0 |   (new block row)
| | **mean dens** | | | | | | | | **233.5** |
Total path-citation instances: 774 across 28 blocks.      (+3 cites, all inside the new row)
== SKILL.md: 16 in-range cite instances, 0 bad; 16 distinct anchors; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0
```

`anchorcheck` output at J5 is **byte-identical** to the freeze output (`cmp` → identical):
the appended registry row introduces no cite anchors it would grade, so all guard fields
stay 0. The `density` delta is confined to the appended block (new block 28; block 27's span
absorbs the separating blank line, 10→11 in its line column, density column unchanged at
544.4 — mechanical accounting, not an edit of the Round-36 block's content). Working-tree
parity: both instruments run in the lane working tree produce outputs **byte-identical** to
the J5 export runs (tracked bytes = J5; the only untracked lane files are wave/dispatch
artifacts and this seat's wave2 writes).

## 3. Verdict

| limb | result |
|---|---|
| 1. additions-only numstat | **28/29 PASS; `corpus/SOURCES.md` 12/9 CONTRADICTED in letter** — 9 deletions are exactly the nine C2-promised row rewrites, zero collateral field change (F1) |
| 2. SKILL.md / PROVINCE.md append-only | **PASS** (byte-prefix proof, stronger than the committed guard) |
| 3. density.py sha256 unchanged | **PASS** (`ee803726…f54710` at base/freeze/J5/working tree; matches guard pin and recorded baseline) |
| 4. instruments behave as recorded | **PASS** (freeze re-run byte-matches all recorded readings; J5 runs clean, anchorcheck byte-identical to freeze) |

**No-harm HOLDS under the guard's contract** (front doors append-only, density instrument
unchanged, zero deleted or renamed tracked paths whole-tree, instruments reproduce their
recorded behavior). One letter-level disagreement is reported as finding F1 with full
field-level evidence; it is the C2 deliverable's promised row decisions, not destruction of
prior content — recommendation: not a no-harm violation, but the seat-criterion/guard
wording tension should be reconciled by the L1.

Guard-strength gaps closed by this seat (attack value): the committed H10 asserts
deleted==0 for the front doors, not byte-prefix append-only — a mid-file pure insertion
into SKILL.md/PROVINCE.md would pass the guard while violating append-only; this seat's
prefix check found none at J5. The guard digests density.py but never executes it; this
seat re-executed both instruments and reproduced the recorded readings byte-for-byte.

## 4. Residual risk / verification gaps

- Y is not yet a commit (receipt untracked at lane tip); the claims' `git diff --name-only
  J Y` = `all-gates.txt` equality is unverifiable until the L1 commits the receipt. If the
  receipt is committed with anything else, that equality breaks — outside this seat's
  reach at attack time.
- Untracked lane files at attack time (`final-gates/`, `wave2/`, `kasegi-r40-falsify.ready*`)
  are dispatch/wave artifacts, not tracked-state changes; the C1 kill rule's "working tree
  clean at filing" was a wave-1 filing-time assertion, not re-judged here.
- `/fast/scratch/hyaku/kasegi-r40` held 1.1G at attack start (wave-1 seat scratch);
  H6's live scratch check is C1's limb, not this seat's — noted, not touched.

## 5. Blast radius and scratch

Writes made: exactly two paths, both inside this seat's allowance —
`.ufo/waves/round-40/wave2/RevNoHarm.md` (this receipt) and
`.ufo/waves/round-40/wave2/RevNoHarm.txt` (outputs fixture). No lane/fleet/sibling/source
file touched; no mutating git/jj command; no campaign tool run in shokuknow; no pacman call.
Scratch `S=/fast/scratch/hyaku/kasegi-r40/RevNoHarm/` (exports, diffs, instrument outputs)
is removed before yield; no `kasegi-r39*`/`r40`-suffixed sibling directory is left behind.
