# ScribeSkillGate — SKILL.md / PROVINCE.md conformance gate (round 34)

Seat: ScribeSkillGate, kasegi-shokunin round 34, wave 1, leaf. Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`,
base `014ee2d7aa8c3c095ff57ae51097606a9906228c`, claims-freeze `29f606dbdd28aff6fd4573ab4b90788bbb90af13`,
HEAD at measurement `206e5108f1190e61b3e2622d21cab8a5d921650c`. Answering model `opencode-go/deepseek-v4.1-flash`
(config route; no model chosen by this seat). Tools installed/upgraded: **none** (no `pacman`, no `uv tool`, no
network fetch — every number below is from committed bytes, the worktree, or the lane's own instruments).

Write scope exercised: `.ufo/waves/round-34/wave1/ScribeSkillGate.md` and
`.ufo/waves/round-34/wave1/ScribeSkillGate/` only. **`SKILL.md` and `PROVINCE.md` were not written** — this seat
reports and proposes; the L1 applies and commits. No `git`/`jj` mutation, no `git add`, no subagent dispatch, no
message to `agent://all`.

## Report

### 1. Verdict (two lines for the lesson Gate)

| file | add-only (0 deletions) | update owed this round | verdict |
|---|---|---|---|
| `SKILL.md` | yes — 0/0 numstat, blob identical base→freeze→HEAD→worktree | **none on measured bytes**; one *conditional* correction if `capture-binding-check.py` is hardened by C1 (§4b) | **PASS (no change, no staleness introduced)** |
| `PROVINCE.md` | yes — 0/0 numstat, blob identical base→freeze→HEAD→worktree | **yes, at integration**: the appended frontier list stops at F16 (`PROVINCE.md:74`) while C2 admits F17 (§4a) | **OPEN — append-only F17 amendment proposed, exact bytes §4a** |

The handoff's expectation ("expected: none beyond this round's no-harm check") holds for `SKILL.md` and does
**not** hold for `PROVINCE.md`: the F17 admission makes the province's own historical frontier list short by one
id, which is the exact defect the `[r31 Frontier amendment …]` and `[r33 Frontier amendment …]` blocks were
appended to prevent.

### 2. Gate A — byte conformance (the requested command, both directions)

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
$ git diff --numstat 014ee2d -- SKILL.md PROVINCE.md          # base -> worktree
$ echo $?
0
$ git diff --numstat 014ee2d HEAD -- SKILL.md PROVINCE.md     # base -> HEAD
$ echo $?
0
$ git diff 014ee2d -- SKILL.md PROVINCE.md | grep -cE '^-[^-]'
0
```

Empty numstat is `0 insertions, 0 deletions` — the add-only condition holds **vacuously**: neither file carries a
round-34 change yet. Blob identity across every rev, plus worktree equality (`git cat-file -p REV:path |
sha256sum` vs `sha256sum path`):

```
$ git rev-parse 014ee2d:SKILL.md 29f606d:SKILL.md HEAD:SKILL.md
cdde78cc6b5b9d6608426a9f3c7354f78700fb0f        (x3, identical)
$ git rev-parse 014ee2d:PROVINCE.md 29f606d:PROVINCE.md HEAD:PROVINCE.md
791ae064a7a641dbe626297b2ca0ecd5628374ba        (x3, identical)
$ git cat-file -p HEAD:SKILL.md    | sha256sum ; sha256sum SKILL.md
b11b60857986c3d735876da168042fe150b8c80fbdf2792263a29cf2a8e3ed84  -
b11b60857986c3d735876da168042fe150b8c80fbdf2792263a29cf2a8e3ed84  SKILL.md
$ git cat-file -p HEAD:PROVINCE.md | sha256sum ; sha256sum PROVINCE.md
b57de5d9517d0ba67a7317d66f5ccc270b4e4a206ace8f27e20e9ec964abd679  -
b57de5d9517d0ba67a7317d66f5ccc270b4e4a206ace8f27e20e9ec964abd679  PROVINCE.md
$ wc -l SKILL.md PROVINCE.md
  1090 SKILL.md
    74 PROVINCE.md
```

The whole round is additions-only in the round's own commit too: `git diff --name-status 014ee2d HEAD` lists 15
paths, **all `A`** (`.ufo/waves/round-34/*`: `claims.json`, `wave1-spec.json`, `wave1-plan.*`, `wave1-run.err`,
`build-spec.py`, `c1-controls/*`, `c2-controls/*`, `census-before.txt`) — no modification, no deletion.

Live worktree at measurement (other seats' writes, none of them mine, none under my scope):

```
$ git status --porcelain --untracked-files=no
 M SCORECARD.md
 M corpus/QUALITY.md
 M corpus/instruments/frontier-recheck-count.py
 M corpus/lessons/round-33.md
 M corpus/source-snapshots/round-32/manifest.json
```

### 3. Gate A' — no-harm checks on the unchanged bytes

```
$ python3 corpus/instruments/anchorcheck.py SKILL.md ; echo $?
== SKILL.md: 12 in-range cite instances, 0 bad; 12 distinct anchors; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0
0
$ python3 corpus/instruments/anchorcheck.py PROVINCE.md ; echo $?
== PROVINCE.md: 0 in-range cite instances, 0 bad; 0 distinct anchors; LOST-RECORDED=0 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0
0
$ python3 corpus/instruments/density.py SKILL.md --label r34-gate ; echo $?
| | **mean dens** | | | | | | | | **201.7** |
Total path-citation instances: 710 across 25 blocks.
0
$ grep -nE '<LANE_HASH>|TODO|FIXME|XXX|PLACEHOLDER' SKILL.md PROVINCE.md ; echo $?
1                     # no match, both files
```

`12 in-range / 0 bad / PIN-BROKEN=0` and mean density `201.7` (710 instances / 25 blocks) are **byte-identical to
the round-33 landed figures** (`.ufo/waves/round-33/wave1/ScribeSkillGate.md` §5) — the expected result for an
unchanged file, recorded so the lesson's No-harm table has a same-instrument before/after pair rather than an
assertion. `PROVINCE.md` has no line-anchored citation surface at all, so its conformance risk is textual (R6
append discipline), not anchor-addressable.

### 4. Gate B — was an update needed?

#### 4a. `PROVINCE.md` — **yes**: F17 append-only amendment (proposed, not applied)

Evidence chain, each link quoted from the lane:

1. The Frontier paragraph names **F01–F11** and the amendments appended after it stop at **F16**:
   `PROVINCE.md:74` = `[r33 Frontier amendment, appended 2026-10-26, end-of-file append per R6] F16 — Chinese crowdsourced-testing platform scope and reward rules (CNVD 众测, 360SRC) — admitted round 33`.
2. The r31 block states the rule it exists to satisfy — header at `PROVINCE.md:54`, and across `PROVINCE.md:56-57`
   the sentence "This amendment appends the four / admissions it does not name, without editing that paragraph:"
   (wrapped by the block's own reflow; both halves quoted here so the line break is not mistaken for an omission).
3. Round 34 admits **F17** as a frozen claim (`claims.json` C2: "Frontier F17 (Immunefi Vulnerability Severity
   Classification System v2.2 — Web3/smart-contract bounty severity classification) admitted 16->17; registry row
   S051 added …"). F17 is inside the province's own frontier semantics — the Core already covers "triage and claim
   gates", and F13 (severity ladders/reward scales, `corpus/README.md:264`) and F14 (severity vocabulary) were
   admitted inside it; Web3/smart-contract severity classification is a sibling object, not a new sub-domain, so
   **no re-scope and no L0 operator question is implied**.
4. Precedent for appending at once is the immediately preceding round (`[r33 …]` appended the same day as F16).
   Precedent for deferring exists too — `git log --oneline -- PROVINCE.md` shows round 30 (F14) did **not** touch
   it and r31 consolidated F12–F15 in one block — so deferral is defensible *if recorded*; immediate append is the
   cleaner default and is what I propose.

Exact append (already in the artifact; **2 lines / 216 B**, `sha256 33f769be3bc6038afd0961d0d20868fbf096f6430d322df07287875b46fafa47`):

```
                                  <- empty line (mirrors the r31/r33 block spacing: PROVINCE.md:73 is blank)
[r34 Frontier amendment, appended 2026-10-26, end-of-file append per R6] F17 — Immunefi Vulnerability Severity Classification System v2.2 (Web3/smart-contract bounty severity classification) — admitted round 34
```

It names no entry path, header field or source id **on purpose**: at measurement none of those exists to be
verified (§5), and the r33 block it mirrors (F16) carries the same title-and-round shape. If the L1 wants the
F15-style binding instead, append this variant *after* checking the landed entry header (the `ground:` value is
**not** in the frozen claim, so do not invent it):

```
… — admitted round 34; row S051, entry corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md (`source: S051`), capture corpus/source-snapshots/round-34/S051.txt
```

Rehearsal (scratch copy, never the lane file), so the L1 can apply without a failed first attempt:

```
$ cp PROVINCE.md $S/PROVINCE.rehearsal.md && cat proposed-PROVINCE-F17-append.txt >> $S/PROVINCE.rehearsal.md
$ wc -l $S/PROVINCE.rehearsal.md
76 $S/PROVINCE.rehearsal.md
$ diff <(head -74 PROVINCE.md) <(head -74 $S/PROVINCE.rehearsal.md) && echo prefix_identical=yes
prefix_identical=yes
$ head -74 PROVINCE.md | sha256sum ; head -74 $S/PROVINCE.rehearsal.md | sha256sum
b57de5d9517d0ba67a7317d66f5ccc270b4e4a206ace8f27e20e9ec964abd679  -
b57de5d9517d0ba67a7317d66f5ccc270b4e4a206ace8f27e20e9ec964abd679  -
$ python3 corpus/instruments/anchorcheck.py $S/PROVINCE.rehearsal.md ; echo $?
== …/PROVINCE.rehearsal.md: 0 in-range cite instances, 0 bad; … PIN-BROKEN=0 … BASE-ABSENT=0
0
```

`PROVINCE.md` currently ends with a single `\n` after the F16 line (verified with `od -c`: `… a d m i t t e d   r o
u n d   3 3 \n`), so the append lands on lines 75–76 and every existing line keeps its number (R6). **Precondition
for applying: C2 must have landed** (row S051, entry, README frontier row). On the tree I measured it has not
(§5), so an append written now would cite an admission the corpus does not yet contain.

#### 4b. `SKILL.md` — **no update owed on measured bytes**; one conditional obligation

The only *live* pin in `SKILL.md` is the round-33 row's re-verify instruction, `SKILL.md:1090`
(`Re-verify: cd <lane> && sha256sum corpus/instruments/capture-binding-check.py (target b4182665…)`). It matches
the bytes:

```
$ sha256sum corpus/instruments/capture-binding-check.py
b4182665ba5cf5441d6495d7de3d59a4c6f8d679d5e9d85c38d16abfb6d0b7f9
$ wc -l corpus/instruments/capture-binding-check.py
492
$ python3 corpus/instruments/capture-binding-check.py --selftest --scratch $S
… 11 × selftest case=… verdict=pass …
selftest cases=11 failures=0
$ echo $?
0
```

That is exactly the row's stated `b4182665…`, `492 lines`, `selftest cases=11`. So the round-33 row is not stale
at this instant.

The round-31 measurement sentence (`SKILL.md:1069`) *looks* stale and is not a defect: it opens with "Measured at
append time (working tree, 2026-10-25)", and two of its values already differ from current bytes —

| pinned at `SKILL.md:1069` | base `014ee2d` | worktree @ measurement | reading |
|---|---|---|---|
| `ledger sha256 c042adf6…` | `c042adf6` | `c042adf6` | matches |
| `counter f926bf75…` | `237fd07c` | `237fd07c` | already differed **at base**; the same sentence carries its own M30-3 "pins behaviour, not one digest" disclaimer |
| `recheck-audit.py 5d4842da…` | `5d4842da` | `5d4842da` | matches |
| `source-recheck.py fd2e01e8…` | `fd2e01e8` | `fd2e01e8` | matches |
| `frontier-recheck-count.py aa60b581…` | `aa60b581` | `2cff234e` | worktree is in flight: `git diff --stat` = `152 insertions(+), 3 deletions(-)` (C1's bidirectional rule A, another seat's write) |

**Conditional obligation:** the round-33 row's `target b4182665…` / `492 lines` / `11 selftest case…` strings
become wrong the moment C1's `capture-binding-check.py` hardening lands (the frozen C1 predicate requires
`selftest cases=N failures=0`, `N>=19`, with nine named cases). If the landed digest differs from `b4182665…`, an
append-only correction is owed at EOF (R6); exact text ready in
`.ufo/waves/round-34/wave1/ScribeSkillGate/proposed-SKILL-r34-correction-TEMPLATE.txt` with `<NEW8>`, `<L>`, `<N>`
to be filled from landed bytes — do **not** apply the template with placeholders. If the file does not move, no
correction is owed and this seat's measurement stands.

**Registry rows for the round's new instruments — not owed by any committed rule.** `SKILL.md` sections exist for
rounds 29/30/31/33 and *not* for round 32, so per-round registration is a precedent, not an invariant. At
measurement neither C1 instrument exists to document:

```
$ ls corpus/instruments/r-defect-closure.sh corpus/instruments/kill-rule-check.py
ABSENT corpus/instruments/r-defect-closure.sh
ABSENT corpus/instruments/kill-rule-check.py
```

If the L1 wants rows for them, they must be written at integration from landed bytes (entry command, verdict map,
self-test string, pinned receipt path); this seat cannot measure them and will not guess. The instruments already
on disk but never registered (`capture-source.py`, `resolution`/`density.py`, `mirror-containment-check.py`,
`resolve-dispatch-check.py`) show the registry is a curated subset — that is why I do not call the omission a gate
failure.

### 5. Mid-wave transient state (recorded, not claimed as defects)

The tree moved under this seat between two capture instants; both are recorded so no later reader mistakes an
in-flight state for a verdict:

| instant (UTC) | `capture-binding-check.py` (no flags) | why |
|---|---|---|
| first pass (untimestamped, before 05:33:39) | `AUDIT records=40 … snapshot_dirs=10 manifest_dirs=9 missing_manifest=1` → `FAIL rule=missing-manifest dir=round-34`, exit 1 | `ScoutSnapshotR34` had written `corpus/source-snapshots/round-34/S051.txt` but not its manifest |
| 05:33:49 (recorded run) | `MANIFEST round-34 records=1 url_bound=0 fetched=1 archival=0`; `AUDIT records=41 … missing_manifest=0`; `FAIL rule=no-row record=S051 dir=round-34`; `records=41 bound=40 unbound=1`, exit 1 | manifest landed; `corpus/SOURCES.md` still at 50 rows |

C2 landing state at the same instant (the reason §4a is a proposal, not an application):

```
$ grep -cE '^\| F[0-9]+ \|' corpus/README.md            -> 16
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md -> 50
$ ls corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md -> No such file or directory (ls_exit=2)
$ sha256sum corpus/source-snapshots/round-34/S051.txt -> 4fd8ed981808b9b9632fd8a4536305e36c82fa98f319bb1cbc7fdb0514b325a5 (175 lines)
```

The round-34 manifest record is strict-UTC (`fetched_utc: "2026-10-26T05:31:10Z"`) and its `sha256` equals the
committed capture digest — that half of the C1/R8 shape already holds; the `no-row` failure is C2's unlanded row,
not a manifest defect.

### 6. Conflicts and caveats (verbatim, for the canonical judge)

1. **Handoff expectation vs measurement.** The item says "expected: none" for skill/province updates. Measured:
   `SKILL.md` none, `PROVINCE.md` amend-warranted at integration (§4a). Reported rather than smoothed.
2. **Pipe artifact, not a verdict.** `python3 corpus/instruments/anchorcheck.py SKILL.md | head -1` returned
   `exit=1` (broken pipe from `head`, first printed line empty) while the unpiped run returns `exit=0` with the
   `== SKILL.md: 12 in-range …` line. Same artifact round 33 recorded; every exit code quoted in §3 is unpiped.
3. **No frozen-claim evidence is claimed here.** Both C1 instruments are absent and no C2 artifact has landed at
   measurement; `SKILL.md`/`PROVINCE.md` conformance is therefore reported as *state plus obligation*, not as a
   verdict on C1 or C2.
4. **`frontier-recheck-count.py` in-flight write is another seat's** (`152 insertions(+), 3 deletions(-)` in the
   worktree); I neither touched it nor judged its diff. It only matters to `SKILL.md:1069` as a dated value.
5. **No file in the lane was written outside my two paths**, and `SKILL.md`/`PROVINCE.md` were left byte-identical
   to base — the add-only gate is measured on a tree whose two subject files I did not modify (the L1 owns the
   append).

### 7. Out of scope (not touched, not judged)

`SCORECARD.md` (ScribeScorecard), `corpus/QUALITY.md` (ScribeQualityDraft/ExecQualityAppends),
`corpus/lessons/round-33.md` and `round-34.md` (ExecLessonErrata / ScribeLesson), `corpus/README.md` frontier row
and `corpus/SOURCES.md` S051 row (ScribeEntryF17 / ExecRegistryAppend), `corpus/source-snapshots/*` manifests,
`corpus/instruments/*` (including the in-flight `frontier-recheck-count.py`), `LOG.md` (the L1), and every C1
closure (r-defect-closure suite, kill-rule matrix, `<LANE_HASH>`, S040 orphan, erratum 2, QUALITY R20 note). No
score claim is made.

### 8. Artifacts

All under `.ufo/waves/round-34/wave1/ScribeSkillGate/`:

| file | content |
|---|---|
| `gate-numstat.txt` | the §2 block verbatim (timestamps, rev-parse triplets, sha256 both sides, status, wc) |
| `pins-and-instruments.txt` | base/HEAD/worktree sha256 prefix + line count per pinned instrument, ledger digest, C1-instrument existence, anchorcheck/density runs |
| `capture-binding-runs.txt` | full `--selftest` (11 cases, `cases=11 failures=0`, exit 0) and the no-flag audit (`records=41 bound=40 unbound=1`, `FAIL rule=no-row record=S051`, exit 1) at 05:33:49Z |
| `anchor-unpiped.txt` | unpiped anchorcheck exit codes and `==` lines for both files |
| `f17-landing-state.txt` | README 16 rows / SOURCES 50 rows / entry absent / S051 capture digest / round-34 dir listing |
| `proposed-PROVINCE-F17-append.txt` | the exact §4a append bytes (2 lines, 216 B, `sha256 33f769be…`) |
| `proposed-SKILL-r34-correction-TEMPLATE.txt` | the conditional §4b correction text with `<NEW8>`/`<L>`/`<N>` placeholders — **template, not appliable as-is** |

Scratch `/fast/scratch/hyaku/kasegi-r34/ScribeSkillGate/` (selftest fixtures, `PROVINCE.rehearsal.md`) removed
before yield; nothing under it is cited as evidence, and two transient `/tmp` anchor dumps were deleted in the
same shell after their `==` lines were copied into `anchor-unpiped.txt`.
