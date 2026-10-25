# RevFixturesC1 — round 28 wave 1 — C1 `--selftest` fixture isolation & completeness review

seat: RevFixturesC1 (reviewer, leaf — no subagent, no background job, no production edit)
lane repo: /home/vgpnk/Projects/shokunin/kasegi-shokunin
claims base: c9f8b115a098c65356e4b3b6048af45a37ab8395 (freeze commit)
recorded_utc: 2026-10-25T17:31:21Z (UTC)
  — the landed instrument (ExecImplC1 landed mid-session: pre-change digest `c2a9e6c6…`
    was observed at session start; live digest moved to `95333e29…` before this review;
    no PRE-STATE label applies to this review — it runs on the landed bytes).
diff cross-check: `.ufo/waves/round-28/wave1/ExecImplC1.diff` body matches
  `git diff -- corpus/instruments/anchorcheck.py` byte-for-byte (only header/footer
  comment lines differ). The diff is the landed change.
lsp note: `xd://lsp` is not mounted (only ast_edit/debug/mcp devices exist); all code-path
  tracing below is textual, grounded in the verbatim landed source lines cited.

---

## 1. Selftest run (verbatim, at landed digest)

Run 1 (from lane root; digest measured before and after):
```
$ python3 corpus/instruments/anchorcheck.py --selftest
selftest cases=9 failures=0
$ echo $?
0
```
Run 2 (determinism): stdout identical, stderr identical (empty), exit 0.
Post-run hygiene: `ls -d /tmp/anchorcheck-selftest-*` → none (temp sandbox removed);
`git status --porcelain` before vs after → identical (no live-tree touch);
instrument digest unchanged across runs (`95333e29…`).

## 2. Fixture inventory — completeness vs kill rule

The kill rule has two directions: (i) a limb with no failing fixture, (ii) a fixture
failing a limb other than its own. Both are covered by construction: the runner asserts
the **complete verdict-class vector** (`want()` defaults every class to 0 and sets exactly
the target; `_counts` parses per-verdict lines plus the summary `in-range` count) and the
**exit code** for every case. 9 cases ship:

| # | case | target limb | expected verdict vector | expected exit |
|---|------|-------------|-------------------------|---------------|
| 1 | missing-file | MISSING-FILE | MISSING-FILE=1, else 0 | 1 |
| 2 | past-eof | PAST-EOF | PAST-EOF=1, else 0 | 1 |
| 3 | outside-base | OUTSIDE-BASE | OUTSIDE-BASE=1, else 0 | 1 |
| 4 | pin-broken | PIN-BROKEN | PIN-BROKEN=1, else 0 | 1 |
| 5 | base-absent | BASE-ABSENT | BASE-ABSENT=1, else 0 | 1 |
| 6 | bounties-absent | BOUNTIES-ABSENT | BOUNTIES-ABSENT=1, else 0 | 1 |
| 7 | bounties-in-range | control (arm positive) | IN-RANGE=1, else 0 | 0 |
| 8 | lost-recorded | control (recorded-not-fail) | LOST-RECORDED=1, else 0 | 0 |
| 9 | clean | control (clean case) | IN-RANGE=1, else 0 | 0 |

All six FAIL_CLASSES limbs have exactly one failing fixture (1–6), plus the required
clean-case control (#9) and two extra controls (#7 bounties arm resolves at all — the arm
must not only fail closed; #8 LOST-RECORDED stays recorded-not-fail). Completeness limb:
**SATISFIED**. (`selftest cases=9 failures=0` — N=9 = 6 limb fixtures + 3 controls.)

## 3. Per-fixture trace — why each fails its limb and no other

All code references are to the landed file lines at digest `95333e29…`.

**#1 missing-file** — fixture: `` `corpus/knowledge/zz-selftest-absent.md:99` ``.
Code path: CITE matches lane-prefixed alternative (line ~156 `_CITE_PATH`); `rel` contains
`/` → lane-base resolution (433) fails; `kind='MIRROR'`, `path=MIRROR/<rel>` (446);
`os.path.exists(path)` false (448); `kind=='MIRROR' and MIRROR_ABSENT` → **false**
(KASEGI_MIRROR env-overridden to a *present* temp root) → `MISSING-FILE` (454).
Why no other limb: base present (not BASE-ABSENT); no pin line in fixture (not
PIN-BROKEN); rel is unprefixed (no OUTSIDE-BASE arm); path not touched (no PAST-EOF);
lone token → no LOST. Expected line: `MISSING-FILE md:1 corpus/knowledge/zz-selftest-absent.md:99`.

**#2 past-eof** — fixture: `` `present.md:9` `` with real temp file `lane/present.md`
(3 lines). Code path: lane dir scan finds the file (433–435) → `kind='LANE'`;
exists → line count 3 < 9 → `PAST-EOF` (458). Why no other: lane file exists (not
MISSING-FILE/BASE-ABSENT); no pin (not PIN-BROKEN); lane rel, no escape arm (not
OUTSIDE-BASE). Expected line: `PAST-EOF md:1 present.md:9 (file has 3 lines)`.

**#3 outside-base** — fixture: `` `~/Projects/bounties/../selftest-escape.md:1` ``.
Code path: bounties arm (408); `realpath(join(root, '../selftest-escape.md'))` =
`<tmp>/selftest-escape.md`; `commonpath(bounties_root, path) != bounties_root` (414–417)
→ `OUTSIDE-BASE`, **before** the absent-root check and before any file access.
Why no other: the within-check precedes BOUNTIES_ABSENT (not BOUNTIES-ABSENT), precedes
isfile (not MISSING-FILE); bounties arm never yields BASE-ABSENT; no pin. Expected line:
`OUTSIDE-BASE md:1 ~/Projects/bounties/../selftest-escape.md:1 (resolved outside <tmp>/…/bounties)`.

**#4 pin-broken** — fixture: pin comment `<!-- pin: pinned.md deadbeef -->` + cite
`` `pinned.md:1` ``; `git init` run in the temp lane dir (306). Code path: `rel in pins`
(369) → `git_show(lane_root, 'deadbeef', 'pinned.md', 1, 1)`; temp repo has no object
`deadbeef` → `git show` rc != 0 → `MISSING` → `PIN-BROKEN` (371–372).
Why no other: pin branch short-circuits all base resolution; the only git touched is the
temp `git init` repo (subprocess env KASEGI_LANE_ROOT=<tmp>/lane ⇒ `git -C <tmp>/lane`);
never the live lane. Expected line:
`PIN-BROKEN md:2 pinned.md:1 (git object missing: deadbeef)`.

**#5 base-absent** — fixture: `` `zz-selftest-ops.mjs:1` ``; `absent=('mirror',)` ⇒
`KASEGI_MIRROR` points at a path that was **not created** (298–299). Code path: lane scan
misses (433); mirror subdir loop misses → `path=MIRROR/<rel>` (444); exists false;
`kind=='MIRROR' and MIRROR_ABSENT` → **true** → `BASE-ABSENT` (449–450).
Why no other: mirror root absent (not MISSING-FILE); UNprefixed path (no escape arm, not
OUTSIDE-BASE); no pin. Expected line:
`BASE-ABSENT md:1 zz-selftest-ops.mjs:1 (base tree absent: <tmp>/…/mirror/zz-selftest-ops.mjs)`.

**#6 bounties-absent** — fixture: `` `~/Projects/bounties/ops/claim-check.mjs:96` ``;
`absent=('bounties',)`. Code path: bounties arm; within check passes (path stays under
root); `BOUNTIES_ABSENT` true → `BOUNTIES-ABSENT` (419–420).
Why no other: distinct arm (not BASE-ABSENT); within-check before isfile (not
MISSING-FILE); root absent (not OUTSIDE-BASE); no pin. Expected line:
`BOUNTIES-ABSENT md:1 ~/Projects/bounties/ops/claim-check.mjs:96 (base tree absent: <tmp>/…/bounties/ops/claim-check.mjs)`.

**#7 bounties-in-range (control)** — fixture: `` `~/Projects/bounties/ops/claim-check.mjs:2` ``
with real temp file `bounties/ops/claim-check.mjs` (3 lines). Code path: within passes;
root present; isfile true → `kind='BOUNTIES'` → range ok → `IN-RANGE` (462–463 with the
bounties kind falling through the `IN-RANGE` else-branch), OK line prints the cited text
`[beta]`. Exit 0. Expected line: `OK md:1 ~/Projects/bounties/ops/claim-check.mjs:2  [beta]`.

**#8 lost-recorded (control)** — fixture: prose trailer
`source: [lost-tree] ~/Projects/bounties/ops/gone.mjs:1-3` (line 1) plus backticked
`` `[lost-base] ~/Projects/bounties/ops/gone.mjs:4` `` (line 2). Code path: TOK is
backtick-only → line 1 never tokenized (so not counted); line 2 tokenized, `LOST.match`
→ `lost=True` → `LOST-RECORDED` bucket and `continue` (465–468), **before** any base
resolution — so the absent bounties root is never consulted. Exit 0 (not a fail class).
Expected line: `LOST-RECORDED md:2 [lost-base] ~/Projects/bounties/ops/gone.mjs:4 (not checked)`
and summary `LOST-RECORDED=1` (not 2).

**#9 clean (control)** — fixture: `` `present.md:2` `` with real temp file
`lane/present.md`. Code path: lane scan finds file → `IN-RANGE(LANE)` (463), exit 0.
Expected line: `OK md:1 present.md:2  [two]`.

## 4. Empirical confirmation (independent replay, not just trace)

Each fixture was replayed outside the runner with the exact same env injection
(`KASEGI_LANE_ROOT/MIRROR/ORIGIN_ROOT/BOUNTIES` → fresh temp dirs). Every case produced
exactly its target verdict class, count 1, zero other verdict lines, and the expected
exit code (1 for #1–6, 0 for #7–9). One representative line per case:

```
missing-file        MISSING-FILE md:1 corpus/knowledge/zz-selftest-absent.md:99        exit=1
past-eof           PAST-EOF md:1 present.md:9 (file has 3 lines)                       exit=1
outside-base       OUTSIDE-BASE md:1 ~/Projects/bounties/../selftest-escape.md:1 …     exit=1
pin-broken         PIN-BROKEN md:2 pinned.md:1 (git object missing: deadbeef)          exit=1
base-absent        BASE-ABSENT md:1 zz-selftest-ops.mjs:1 (base tree absent: …)        exit=1
bounties-absent    BOUNTIES-ABSENT md:1 ~/Projects/bounties/ops/claim-check.mjs:96 …   exit=1
bounties-in-range  OK md:1 ~/Projects/bounties/ops/claim-check.mjs:2  [beta]           exit=0
lost-recorded      LOST-RECORDED md:2 [lost-base] ~/Projects/bounties/ops/gone.mjs:4  exit=0
clean              OK md:1 present.md:2  [two]                                         exit=0
```

## 5. Live-tree isolation (temp-dir limb)

- Every fixture lives under `tempfile.mkdtemp(prefix='anchorcheck-selftest-')`, removed in
  a `finally: shutil.rmtree(base, ignore_errors=True)` (289, 330). Post-run probe: no
  `/tmp/anchorcheck-selftest-*` leftovers.
- Every case runs the instrument as a **subprocess with KASEGI_* env overrides** (311–317),
  so the module-level roots are re-derived inside each isolated process — correct, because
  the roots are module-level constants (123–147) and in-process `os.environ` mutation would
  not re-derive them.
- `git init`/`git -C` only ever touch the temp repo; the live lane repo is never a git
  target of any fixture (the only live-repo use in the binary is the normal
  `git_show` for pins in normal mode).
- Empirical proof of no live-tree mutation: `git status --porcelain` byte-identical before
  and after the two `--selftest` runs; instrument digest unchanged; no temp leftovers.
- The clean control (#9) additionally proves the gate is not unconditionally fail-closed:
  exit 0, IN-RANGE=1.

## 6. Interplay with the frozen counters (no regressions)

- `BOUNTIES-ABSENT` is printed as a verdict line **before** the summary (it is in
  `_PRINT_FIRST`, 505) and is deliberately **not** a summary bucket (docstring, ~87–91) —
  so `grep -c BOUNTIES-ABSENT` on the bounties-fixture output is 1, exactly the C1(b)
  after-value. (The replay above reproduces that single line.)
- `BASE-ABSENT` remains printed after the summary (not in `_PRINT_FIRST`) — behavior
  unchanged from r19.
- The C1(d) no-harm gate was spot-run on the live SKILL.md:
  ```
  skill_exit=0
  == SKILL.md: 7 in-range cite instances, 0 bad; 7 distinct anchors; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0
  ```
  matching the frozen after-values (exit 0, bad=0, LOST-RECORDED=306, BASE-ABSENT=0).

## 7. Findings

**No kill-condition defect found.** Both directions of the kill rule are satisfied:
every limb has a failing fixture, and no fixture fails a limb other than its own
(verified by code trace and by empirical replay). `selftest cases=9 failures=0`, exit 0,
deterministic across two runs, at the landed digest `95333e29…`.

Minor observations (non-blocking, no behavior change):
1. **Dead branch (line 451–452):** `elif kind == 'BOUNTIES' and BOUNTIES_ABSENT:`
   is unreachable — `kind='BOUNTIES'` is only assigned after `os.path.isfile(path)`
   succeeds (424), i.e. when the file exists, so the exists-branch can never see
   `BOUNTIES_ABSENT`. It mirrors the MIRROR guard (449) but the MIRROR assignment happens
   before the existence check. Harmless; could be removed or documented.
2. **Unexercised bounties-arm subpaths:** no fixture drives the bounties arm's
   `MISSING-FILE` (421–422) or `PAST-EOF` (through the shared 456–458 path) branches —
   the classes are exercised via the mirror (#1) and lane (#2) fixtures, so the kill rule
   is unaffected, but two arm-local branches lack direct fixture coverage.
3. **`_counts` IN-RANGE sentinel:** `-1` is used as a fail marker when the summary line is
   missing (203). Sound, but relies on the summary regex; a child crashing before printing
   a summary yields IN-RANGE=-1 and is caught. Fine.
4. **Fixture #8 comment vs behavior:** the fixture carries the expected `[lost-tree]`
   prose trailer; the code treats non-backticked text as non-tokens, so the LOST count is
   1. This matches the corpus disclosure (4 marked bounties cites → LOST-RECORDED).
5. **Git init noise:** `git init` may read global gitconfig; it ran clean in both live
   runs, and even a failure would still yield PIN-BROKEN via `git show` rc!=0 (the pin
   object is fake in every case), so the limb is robust to git config variance.

## 8. Residual risk / verification gaps

- The `--selftest` receipt-index integration (assemble-receipts.py / c1-receipt-index.txt)
  is not reviewed here; it is ExecReceiptCanonC1's scope.
- C1(a)/(b)/(d) counters (bad-fixture exit, bounties-fixture line count, SKILL.md live)
  are ExecFixtureRun/ExecNoHarmC1 scope; I only spot-checked no-harm (above) as part of
  fixture-context verification.
- Determinism was measured over two runs on the landed bytes (identical); a longer
  stress is not required by the claim.

VERDICT: **PASS** — selftest fixtures are isolating and complete under the frozen kill
rule; selftest runs green at the landed digest; no live-tree contact observed.
No re-run command needed from the L1 for this seat (review ran on landed bytes).
