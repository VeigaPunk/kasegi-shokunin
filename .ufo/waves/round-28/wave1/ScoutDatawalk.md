# ScoutDatawalk — round-28 wave 1, kasegi-shokunin

Seat: bounded data-walk (facts only, no production edit). Date 2026-10-25 (UTC).
Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Lane base revision per dispatch: `c9f8b115a098c65356e4b3b6048af45a37ab8395` (the round-28 claims freeze commit).
Lane HEAD at measurement start: `94f387cbee71a532a51ce075f01701a557231e85` (round-28 wave1 spec + dispatch;
`c9f8b11` is its parent, `261a6651b7e52c58e9ad0ceaef6f3bd0bf2d904f` is the freeze commit's parent and is the
`"base"` field value inside `claims.json`).

No production file was written by this seat. The only artifact this seat created is a scratch instrument copy
under its own seat directory (`.ufo/waves/round-28/wave1/ScoutDatawalk/anchorcheck-probe.py`), used to test
hypotheses about the C1 arm without touching `corpus/instruments/anchorcheck.py`.

## Method — two independent base reproductions

Because sibling seats were already mutating the worktree during this seat's run, **every BEFORE value was
re-measured against the frozen base bytes**, not against the live tree:

- **Base archive**: `git archive c9f8b11 | tar -x -C $(mktemp -d)` → `/tmp/kasegi-base-W6KNse` (read-only).
- **Base clone**: `git clone --no-hardlinks . $C && git checkout c9f8b11` → `/tmp/kasegi-clone-9Wj9zj`
  (a real `.git`, so `git ls-files`/`git ls-tree` and the census `--file` mode are exercised properly).

Both reproductions agree with each other and with the committed before-receipts. Commands below are run
from the lane root and are stated verbatim so the L1 can re-run them.

---

## 1. Frozen counters — BEFORE values at base `c9f8b11`

All six counter families hold their BEFORE values at the frozen base. Every number below was **measured**,
not copied from the receipts.

| Counter | Expected | Measured at base `c9f8b11` | Verdict |
|---|---|---|---|
| bad-fixture exit (`anchorcheck.py .ufo/waves/round-27/c1-controls/bad-fixture.md`) | 0, BASE-ABSENT=1 | `exit=0`; summary `LOST-RECORDED=0 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=1` | HOLD |
| bounties-fixture `grep -c BOUNTIES-ABSENT` | 0 | `0` (grep exit 1, no match) | HOLD |
| `frontier-recheck-count.py` | entries=14 pass=14 exit=0 | `entries=14 pass=14 exit=0`, process exit 0 | HOLD |
| frontier admitted (`awk` on `corpus/README.md`) | 11 | `11` | HOLD |
| sources census | exit 0, 41 rows | 41 rows; `sources-census.sh validate --file <base>/corpus/SOURCES.md` → `W04 S028`, `W04 S029`, `ok`, **exit=0** | HOLD |
| SKILL.md live run (C1 no-harm) | exit 0, bad=0, LOST-RECORDED=306 | `exit=0`; `== SKILL.md: 7 in-range cite instances, 0 bad; 7 distinct anchors; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0` | HOLD |

Verbatim base outputs:

```
$ cd <base> && python3 corpus/instruments/anchorcheck.py .ufo/waves/round-27/c1-controls/bad-fixture.md >/dev/null 2>&1; echo $?
0
$ cd <base> && python3 corpus/instruments/anchorcheck.py .ufo/waves/round-27/c1-controls/bad-fixture.md
== .ufo/waves/round-27/c1-controls/bad-fixture.md: 0 in-range cite instances, 0 bad; 0 distinct anchors; LOST-RECORDED=0 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=1
BASE-ABSENT md:2 corpus/knowledge/zz-r27-anchorcheck-missing.md:99 (base tree absent: /home/vgpnk/Projects/the-bounty-hunter/corpus/knowledge/zz-r27-anchorcheck-missing.md)
$ cd <base> && python3 corpus/instruments/anchorcheck.py .ufo/waves/round-27/c1-controls/bounties-fixture.md 2>/dev/null | grep -c BOUNTIES-ABSENT
0
$ cd <base> && python3 corpus/instruments/anchorcheck.py SKILL.md >/dev/null 2>&1; echo $?
0
```

The base bad-fixture receipt `.ufo/waves/round-28/c1-controls/bad-fixture-before.txt` was byte-compared
against a fresh re-run: **MATCHES**. The committed round-28 before-receipts are genuine fresh re-runs of
the committed round-27 fixtures, not re-creations (round-27 lesson carry-forward 1 satisfied).

### Base instrument digests (for the receipt index)

| File | sha256 at base `c9f8b11` | note |
|---|---|---|
| `corpus/instruments/anchorcheck.py` | `c2a9e6c6088015968b3c6ea7f12a0ea66699c3ecb2a21db362659db8e95ef748` | matches the frozen `before.instrument_sha256` exactly |
| `corpus/instruments/recheck-audit.py` | `3fc0d751f2a5819879d440f8ef62b607376a8b6914d7edf9fe1b2fc25662d4e1` | C1's `c2a9e6c6…` digest is `anchorcheck.py`, a different instrument — do not conflate them |
| `corpus/instruments/knowledge-expected.txt` | `30ba586029f679721d57025a1ac339b93fe11b38c5825c721be495048b2a9080` | 41 physical lines, 39 entry lines |

Base `anchorcheck.py` blob digest was taken from the git object (`git show c9f8b11:corpus/instruments/anchorcheck.py | sha256sum`),
not from the live file — the live file had already changed under a sibling seat by then.

---

## 2. Knowledge-entry count — the dispatch expectation of 41 does **not** hold; 39 does

Dispatch item 2 asked for `git ls-files corpus/knowledge/*.md | wc -l` = **41**. Measured value is **39**.

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && git ls-files corpus/knowledge/*.md | wc -l
39
$ git ls-tree -r --name-only c9f8b11 -- corpus/knowledge/ | wc -l
39
$ git ls-tree -r --name-only c9f8b11 -- corpus/knowledge/ | grep -v '\.md$' | wc -l
0
$ ls corpus/knowledge/*.md | wc -l          # base archive
39
```

There are **no non-`.md` files** directly under `corpus/knowledge/`, so the tracked set and the on-disk set
are the same 39 files. **No untracked knowledge file existed at base** (base clone `git status --porcelain
corpus/knowledge/` → empty).

The number **41** is a different measurement: `wc -l corpus/instruments/knowledge-expected.txt` = 41, which
is **39 entry lines + 2 `#` header comment lines**. The instrument's own `load_expected()` skips blanks and
`#` comments, so its entry count is 39. The round-27 lesson's "41" and the round-26 integration's "39" were
never in conflict — they counted different things. This is exactly the round-27 carry-forward 4
reconciliation, and it is already independently documented by the `ExecExpectedList` seat.

**Consequence for the L1 (important):** the expected-list file is **still at 39 entries** in the live tree
(sha256 `30ba5860…`, unchanged from base) while the F12 entry has landed. The live `recheck-audit.py`
therefore currently exits **1**:

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/recheck-audit.py
strict pass=40/40 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=16 gated=24 broken=0
lines=40 total=40 pass=40 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=1
expect=present expected=39 missing=0 unexpected=1 exit=1
```

The stale list is the only red line: `unexpected=corpus/knowledge/japanese-domestic-disclosure-workflow.md`.
Regeneration must produce **40 entry lines (42 physical lines)** — lane-relative paths, run from the lane
root. The `ExecExpectedList` seat report carries the exact command; this seat did not run it (read-only
seat, and the file is owned by the C1/C2 integration path).

Base reference value for the same command (base clone, `--cdroot` pointed at the lane root because the
entries' `recheck:` lines hard-code the lane path):

```
strict pass=39/39 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=15 gated=24 broken=0
lines=39 total=39 pass=39 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=39 missing=0 unexpected=0 exit=0
```

> Note for the L1: running `recheck-audit.py` from a scratch copy of the corpus without `--cdroot <lane root>`
> makes all 38 strict limbs fail (`strict pass=1/39 … exit=1`) — the entries' `recheck:` lines `cd` to the
> absolute lane path, so the scratch copy is not the cd target. This is a measurement-setup artifact, not a
> corpus defect. The base clone with `--cdroot` reproduces the lane's own exit 0.

---

## 3. `claims.json` is byte-exact with the freeze commit

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
$ git show c9f8b115a098c65356e4b3b6048af45a37ab8395:.ufo/waves/round-28/claims.json | sha256sum
b785cb01c4442ee9d4d23596194e0545d79a9d790db3c7b3133ecd285d6016de  -
$ sha256sum .ufo/waves/round-28/claims.json
b785cb01c4442ee9d4d23596194e0545d79a9d790db3c7b3133ecd285d6016de  .ufo/waves/round-28/claims.json
$ git diff c9f8b11 -- .ufo/waves/round-28/claims.json
(no output)
```

**Confirmed byte-exact.** The worktree file is unmodified relative to the freeze commit, and the freeze
commit's parent `261a6651b7e52c58e9ad0ceaef6f3bd0bf2d904f` is the value of the `"base"` field inside
`claims.json` — the freeze commit's own parent, so the two are consistent.

---

## 4. The 4 disclosed corpus bounties-marked citations — they exist, but the frozen *effect* does not reproduce

**Existence (dispatch item 4) — CONFIRMED.** Each of the four named files carries exactly one marked
bounties provenance citation, in the anchored `path:NN` form:

```
corpus/knowledge/claim-gates.md:123:                  source: [lost-tree] ~/Projects/bounties/ops/claim-check.mjs:1-233, tag 014A; full round-3 source read.
corpus/knowledge/intake-and-finalize.md:109:          source: [lost-tree] ~/Projects/bounties/ops/import-board.mjs:1-258, ops/finalize-all.mjs:1-80, ledger/imports.jsonl, and claims/ verification.
corpus/knowledge/mission-control.md:169:               source: [lost-tree] ~/Projects/bounties/ops/fleet-dispatch.mjs:1-427 and fleets/missions, fleets/run, leases, priority, and state-snapshot inventories.
corpus/knowledge/source-tree-loss-2026-09-28.md:353:   source: [lost-tree] ~/Projects/bounties/PROVINCE.md:3 and the 2026-09-28 source-tree census; lane round-15 loss record with round-19 absence errata.
```

`grep -cE '^source: *\[lost-(tree|base)\] *~/Projects/bounties/[A-Za-z0-9_./-]+:[0-9]'` returns **1 in each of
those four files** and 0 in all 35 others. These four are, in fact, the *only* four corpus files whose
bounties provenance line carries the anchored `path:NN` form — 18 files have a `source: [lost-*] ~/Projects/bounties…`
line in some form, and 14 of those are unanchored (no `:NN`).

**The frozen *effect* — does not reproduce under a CITE-arm-only change.** The frozen `C1.corpus_disclosure`
cell asserts these 4 "newly classify LOST-RECORDED instead of being silently skipped" after the CITE arm.
Measured, that is **false**, and the reason is mechanical:

- `anchorcheck.py` extracts candidates with `TOK = re.compile(r"`([^`\n]+)`")` — **backticked spans only**.
- The four `source:` lines above are **plain prose, not backticked**.
- Therefore CITE never sees them, before or after the arm.

Verified two ways at base bytes:

```
$ grep -rnoE '`[^`]*~/Projects/bounties[^`]*:[0-9]+(-[0-9]+)?`' corpus/knowledge/ SKILL.md ; echo $?
1        # zero hits lane-wide
```

and by a scratch instrument copy with **only** the `~/Projects/bounties/` CITE arm added (no other change):
a full sweep over all 39 corpus entries + SKILL.md shows **zero verdict-class movement anywhere** —
`LOST-RECORDED` unchanged in every file (`claim-gates 0`, `intake-and-finalize 0`, `mission-control 0`,
`source-tree-loss-2026-09-28 15`, `SKILL.md 306`).

This **independently reproduces** the L1's `claims-erratum-1.md` correction (which supersedes the frozen
disclosure cell with "zero backticked anchored `~/Projects/bounties/` citations exist; no verdict-class count
moves on any file"). No further correction is needed; this seat's measurement agrees with the erratum.

**Additional finding the L1 may want (new information beyond the erratum):** the four named files are
*precisely* the four that would move — but only if the instrument additionally scanned **bare (unbackticked)
`source:` header lines**. A scratch probe that adds exactly that (extract the anchored `path:NN` from a
`^source: [lost-*] …` line and feed it through the normal LOST→CITE path) yields:

| File | base LOST-RECORDED | with source-line scan | moves? |
|---|---|---|---|
| `claim-gates.md` | 0 | 1 | yes |
| `intake-and-finalize.md` | 0 | 1 | yes |
| `mission-control.md` | 0 | 1 | yes |
| `source-tree-loss-2026-09-28.md` | 15 | 16 | yes |
| all 35 other entries + SKILL.md | — | unchanged | no |

So the frozen disclosure cell describes a *different* implementation than the one landed (the landed
instrument's own selftest case 8 asserts the opposite: the bare `source: [lost-tree] ~/Projects/bounties/ops/gone.mjs:1-3`
trailer "is deliberately NOT a token (TOK is backtick-only)"). The erratum's wording is the correct one for
the landed bytes. **No production change is warranted by this finding** — it is recorded so the L1 does not
chase the frozen cell as an unmet counter.

---

## 5. `recheck-audit.py` — summary lines

**Base `c9f8b11`** (base clone, `--cdroot` at the lane root):

```
strict pass=39/39 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=15 gated=24 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
lines=39 total=39 pass=39 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=39 missing=0 unexpected=0 exit=0
```

Process exit **0**. The expected-list basis at base is **39 entries** (`expected=39 missing=0 unexpected=0`),
matching the 39 tracked corpus entries exactly.

**Live tree at measurement time** (F12 entry landed, expected list not yet regenerated):

```
strict pass=40/40 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=16 gated=24 broken=0
lines=40 total=40 pass=40 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=1
expect=present expected=39 missing=0 unexpected=1 exit=1
```

Process exit **1**, sole cause `unexpected=corpus/knowledge/japanese-domestic-disclosure-workflow.md`.
Everything else is green: the new entry's own `recheck:` line parses, resolves its paths, and passes all
six strict limbs (`strict pass=40/40`).

---

## Additional observed state (context for the L1, not a verdict)

Recorded because the L1's C2 after-values depend on them and this seat measured them at the live tree:

- **Frontier harness (live)**: `entries=15 pass=15 exit=0`, including
  `PASS F12 knowledge/japanese-domestic-disclosure-workflow.md ids=S041,S042 exit=0` → the C2 after-value
  `entries=15 pass=15 exit=0` is **already met** in the live tree.
- **Frontier admitted (live)**: `12` (the `F12` row is present and `admitted` in `corpus/README.md`) →
  C2 after-value `frontier_admitted=12` **met**.
- **S042 registry row (live)**: exactly 1 row matching `^\|[[:space:]]*S042[[:space:]]*\|`; SOURCES row count
  is now **42**; census `validate` → `W04 S028`, `W04 S029`, `ok`, **exit=0** → C2 after-value
  `sources_rows=42, census exit 0` **met**.
- **S041 used-by**: the base cell was
  `corpus/knowledge/iso-29147-and-30111-division-of-labour.md, corpus/knowledge/iso-29147-divergence-and-clause-crosswalk.md`;
  the live cell appends `corpus/knowledge/japanese-domestic-disclosure-workflow.md`, and the old→new
  transition is logged in the `## Changes` block of `corpus/SOURCES.md` (S041 used-by cell old → new).
- **Round-28 captures**: `corpus/source-snapshots/round-28/S041.txt` sha256
  `e18acbf99d137c262c1f08c6f0f92887236641ec8abcccfc7470247242f5ab47` — **byte-identical** to the round-26
  capture (`cmp` reports no difference); `S042.txt` sha256
  `b432ec165693d005fa5de326ffb40d60d0476b18a345a9fc6d631d10b9c96966`.
  `corpus/source-snapshots/round-28/manifest.json` pins both (path stem == id), 6 Q-assertions each.
  `source-recheck.py --manifest corpus/source-snapshots/round-28/manifest.json --source S041 --source S042`
  → all 12 quote assertions `OK occurrences=1`, **exit 0**.
- **Landed C1 instrument (live, sibling seat's product)**: sha256
  `95333e29ee5acce549f8e0b6328c6dcab3c542cf16bc295d6a6ae70c6f144514`;
  bad-fixture exit **1**, bounties-fixture BOUNTIES lines **1**, `--selftest` → `selftest cases=9 failures=0`
  exit 0, SKILL.md live run exit 0 with `LOST-RECORDED=306`, bad=0, `BASE-ABSENT=0 PIN-BROKEN=0 OUTSIDE-BASE=0`
  → the C1 after-values are met in the live tree.
- **Live untracked knowledge file**: `corpus/knowledge/japanese-domestic-disclosure-workflow.md` is present but
  untracked (sibling seat's product, awaiting the L1's commit). Base had none.

## Re-run commands for the L1 (post-change)

```bash
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
python3 corpus/instruments/anchorcheck.py .ufo/waves/round-27/c1-controls/bad-fixture.md >/dev/null 2>&1; echo "bad_exit=$?"
python3 corpus/instruments/anchorcheck.py .ufo/waves/round-27/c1-controls/bounties-fixture.md 2>/dev/null | grep -c BOUNTIES-ABSENT
python3 corpus/instruments/anchorcheck.py --selftest; echo "selftest_exit=$?"
python3 corpus/instruments/anchorcheck.py SKILL.md >/dev/null 2>&1; echo "skill_exit=$?"
python3 corpus/instruments/anchorcheck.py SKILL.md 2>/dev/null | grep '^== SKILL.md'
sha256sum corpus/instruments/anchorcheck.py
python3 corpus/instruments/frontier-recheck-count.py | tail -2
awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md
grep -cE '^\|[[:space:]]*S042[[:space:]]*\|' corpus/SOURCES.md
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi; echo "census_exit=$?"
python3 corpus/instruments/recheck-audit.py | tail -4; echo "audit_exit=$?"   # expected 0 AFTER the expected list is regenerated to 40 entries
git ls-files corpus/knowledge/*.md | wc -l                                       # 39 tracked + 1 untracked F12 entry → 40 after commit
```

## Honesty / tooling note

No tool was installed or upgraded by this seat; no pacman transaction was attempted (host-wide pacman pause
still in force). Scratch artifacts this seat created, all outside the lane's production paths and all
removable at round close: `.ufo/waves/round-28/wave1/ScoutDatawalk/anchorcheck-probe.py` (scratch instrument
copy), `/tmp/kasegi-base-W6KNse` (base archive), `/tmp/kasegi-clone-9Wj9zj` (base clone). Every number in
this report was produced by a command that ran; no value is inferred, and no check is reported as passed
that was not executed.

## Confidence and remaining unknowns

- **High confidence**: all BEFORE values (measured twice, two independent base reproductions, and matching
  the committed before-receipts); `claims.json` byte-exactness; the 39-vs-41 count-basis distinction; the
  mechanical reason the frozen C1 disclosure cell does not reproduce; the live C2 after-values already met.
- **Unknown / out of this seat's scope**: whether the L1 will regenerate the expected list (the one remaining
  red line, `recheck-audit` exit 1); whether the round-28 lesson will carry the C1 disclosure correction
  forward verbatim from `claims-erratum-1.md` (this seat recommends it, and notes that the erratum's wording
  is the one that matches the landed bytes); the quality of the S042 IPA capture and its Q9 quotes
  (independently re-verified here only as *exactly-once* and *sha256-bound* — not as semantically correct).
