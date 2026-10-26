# ScribeShonen — `SHONEN.md` round-33 evidence refresh (wave 1)

Seat: `ScribeShonen` (scribe). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`
(round 33, dispatched by `KasegiR33`; lane base `690b69da`, claims freeze `6e55c8d`).
Owned path exercised: `SHONEN.md` (only). Second write: this receipt.
Date: 2026-10-26. Lane HEAD seen at write time: `9f98488` (wave-1 integration).
Answering model as recorded by the harness route table: `opencode-go/deepseek-v4.1-flash`
(no model passed by this seat, bound 10). Tools installed/upgraded: none.

## 0. Bounds compliance

- Writes: `SHONEN.md` and this receipt, both lane-relative. No git/jj mutation (read-only
  `log`/`show`/`diff`/`status`/`rev-parse` only), no fetch, no install, no subagent dispatch,
  no background job, no live-target contact, no credential material.
- R6 + `ConnOwnership` flag honoured: **same-line replacement only**. `wc -l` before and after
  = 42, so every line keeps its number (including `:34`, cited by
  `corpus/lessons/round-31-verifier-spotcheck.md:23` and `:107`). The four `[~]` bullets
  (`:5`, `:15`, `:24`, `:36`) are untouched; no `[x]` was introduced.
- Scratch: none created (read-only seat). Nothing written to `/tmp`; no `$HYAKU_SCRATCH` tree
  was needed, so no cleanup debt.

## 1. Pre-edit state

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
$ git show HEAD:SHONEN.md | sha256sum ; git show HEAD:SHONEN.md | wc -l
2d4468a2dd3e91b3638bb1c40d02fb6b7fa66b82f634c6048810292490d01436  -
42
$ git diff --numstat 690b69da 9f98488 -- SHONEN.md
                                   # (empty: no round-33 commit touched SHONEN.md)
$ grep -c '^\s*- \[~\]' SHONEN.md   # 4 boxes, all [~] with round-31 evidence
```

## 2. Evidence read (commands and the numbers taken from them)

Every number below was read out of a receipt or a read-only command, never from memory.

### 2.1 Box 1 — SKILL.md decision tables / density / anchorcheck

`wave1/ExecRegressionC1.md` §2.8/§2.9 (raws `wave1/ExecRegressionC1/{anchor.txt,density-final.txt,density-base.txt}`)
and §2.10:
`12 in-range cite instances, 0 bad`, `PIN-BROKEN=0`, `LOST-RECORDED=306`, `anchor_exit=0`;
mean dens `201.7` over 25 blocks / 710 citations vs base `191.5` / 24 / 689, both `exit=0`;
`git diff --numstat 690b69da -- SKILL.md` = `19	0`.
Cross-checked against `wave1/ExecNoHarmFinal.md` §3/§4 (`191.5 → 201.7`; base 7 OK → 12 OK,
`0 bad`, same fail classes) and `wave1/ScribeSkillGate.md` §4/§5 (1090 lines, sha256
`b11b6085…a8e3ed84`) — its §5 does not itself state the mean, hence the ExecRegressionC1 pointer.

### 2.2 Box 2 — end-to-end task in LOG.md

```
$ grep -n '^## Round' LOG.md | tail -3
1584:## Round 31 — 2026-10-25 — one-limb mutation ledger … + F15 … admitted
1593:## Round 32 — 2026-10-25 — honest stop: … no seat ran … re-dispatched as round 33
$ grep -c '^## Round 33' LOG.md
0
$ git log -1 --oneline -- LOG.md
6e55c8d round-33: freeze claims C1/C2 ..., LOG r32 entry (D1)
$ git diff --numstat 690b69da 9f98488 -- LOG.md
4	0	LOG.md
$ wc -l LOG.md
1595 LOG.md
```

The round-32 entry is the honest stop (not an end-to-end task); the round-33 end-to-end
measurement exists only as receipts: `wave1/ExecRegressionC1.md` §2.1/§2.2 —
`records=40 bound=40 unbound=0` twice with `run1_exit=0 run2_exit=0` and
`selftest cases=11 failures=0`, `selftest_exit=0`. `LOG.md` is the L1's path, so the box stays `[~]`.

### 2.3 Box 3 — instructions executable without oral context

- `wave1/ExecRegressionC1.md` §2.5 (raw `recheck.txt`): `strict pass=45/45 cdroot_fail=0
  instrument_fail=0 own_fail=0`, `expect=present expected=45 missing=0 unexpected=0`,
  `recheck_exit=0`.
- `wave1/ExecExpectedList.md` §3: the same after-state on quiescent bytes; `knowledge-expected.txt`
  sha256 `3f68b9a2…ab81ceb`, 44 → 45 entries.
- `wave1/ExecHarnessC2.md` §C2.[7]: `PASS     F16  knowledge/chinese-crowdsourced-testing-scope-and-rewards.md ids=S049,S050`,
  `entries=19 pass=19 exit=0`.
- `wave1/ExecHarnessC2.md` §C2.[8]/[9]: S049 `sha256 OK` + `Q1`-`Q8` `OK occurrences=1`
  (`recheck49_exit=0`); S050 `sha256 OK` + `Q1`-`Q6` (`recheck50_exit=0`).
- `ls corpus/knowledge/*.md | wc -l` → `45`.

### 2.4 Box 4 — PROVINCE.md accuracy / no bleed

- `wave1/ScribeProvince.md` §5: EOF append only, `git diff --numstat -- PROVINCE.md` = `2	0`,
  `grep -c '^-[^-]'` = 0; PROVINCE is 74 lines (measured below).
- `wave1/ConnSibling.md` §1/§3/§4 + Findings: `scoped-terms=0` in all six sibling lanes for
  `CNVD|360SRC|众测|zc.cnvd.org.cn|security.360.cn|crowdsourced`; `kake-shokunin/corpus/README.md:464-465`
  disclaims vulnerability handling; Province verdict: F16 sits inside kasegi.

## 3. The edit

Four same-line hunks over the four evidence blocks; every bullet and blank line byte-identical:

```
$ git diff -U0 -- SHONEN.md | grep -E '^@@'
@@ -6,8 +6,8 @@ Promotion to shokunin requires all of:
@@ -16,7 +16,7 @@ Promotion to shokunin requires all of:
@@ -25,10 +25,10 @@ Promotion to shokunin requires all of:
@@ -37,6 +37,6 @@ Promotion to shokunin requires all of:
$ git diff -U0 -- SHONEN.md | grep -cE '^[-+]- \[[~ ]\]'
0
$ git diff --numstat -- SHONEN.md
31	31	SHONEN.md
```

What each box now claims (round-33 observable state, all pointers resolvable in the lane):

1. SKILL.md: sha256 `b11b60857986c3d735876da168042fe150b8c80fbdf2792263a29cf2a8e3ed84`, 1090 lines,
   append-only `19	0`; density `201.7` / 25 blocks / 710 cites vs base `191.5` / 24 / 689;
   anchorcheck `12 in-range … 0 bad`, `LOST-RECORDED=306`, `PIN-BROKEN=0`.
2. LOG.md: newest entry `## Round 32` at `:1593` (honest stop, appended by the L1 in `6e55c8d`),
   last end-to-end entry `## Round 31` at `:1584`, no `## Round 33` heading, round-33 measurement
   unlogged; box stays `[~]`.
3. 45 knowledge entries each with one `recheck:`; `strict pass=45/45`, `expected=45 missing=0
   unexpected=0`; harness `entries=19 pass=19 exit=0` with `PASS F16 ids=S049,S050`; S049/S050
   source-recheck exit 0 with their Q counts.
4. PROVINCE.md: EOF F16 amendment only (`2	0`, 0 deletions, 74 lines, sha256 `b57de5d9…abd679`),
   F16 inside the province, six-lane sweep zero hits.

## 4. Post-edit verification (read-only)

```
$ wc -l SHONEN.md
42 SHONEN.md
$ sha256sum SHONEN.md
a8d7d203767376aeb7afd9025d77c7a7687aacf1d386dd847722d563afdc008a  SHONEN.md
$ grep -c '^\s*- \[~\]' SHONEN.md ; grep -c '\[x\]' SHONEN.md
4
0
$ git status --porcelain -- SHONEN.md
 M SHONEN.md
$ wc -l SKILL.md PROVINCE.md LOG.md
  1090 SKILL.md
    74 PROVINCE.md
  1595 LOG.md
$ sha256sum SKILL.md PROVINCE.md LOG.md corpus/instruments/capture-binding-check.py corpus/instruments/knowledge-expected.txt
b11b60857986c3d735876da168042fe150b8c80fbdf2792263a29cf2a8e3ed84  SKILL.md
b57de5d9517d0ba67a7317d66f5ccc270b4e4a206ace8f27e20e9ec964abd679  PROVINCE.md
52c04d267453881d0caba372c46497f0590df081399b54b8dc8ef7ba133cf5f8  LOG.md
b4182665ba5cf5441d6495d7de3d59a4c6f8d679d5e9d85c38d16abfb6d0b7f9  corpus/instruments/capture-binding-check.py
3f68b9a2ff7db654770bc11cb3b178b3d2920cc8e5ca0ba9761d85a65ab81ceb  corpus/instruments/knowledge-expected.txt
$ git show 9f98488:SKILL.md | sha256sum ; git show 9f98488:PROVINCE.md | sha256sum
b11b60857986c3d735876da168042fe150b8c80fbdf2792263a29cf2a8e3ed84  -
b57de5d9517d0ba67a7317d66f5ccc270b4e4a206ace8f27e20e9ec964abd679  -
```

The cited digests equal the integration-commit bytes (`git show 9f98488:`), so the evidence
lines describe committed state, not an in-flight draft.

## 5. Findings and disclosures

1. **Delivery note.** `SHONEN.md` is modified in the worktree only; the L1's wave-1 integration
   commit `9f98488` predates this edit (`git diff --numstat 690b69da 9f98488 -- SHONEN.md` empty).
   The L1 must commit it through the lane helper.
2. **Routed round-31 defect 2 is superseded, not errata'd.** The old `:34` sentence
   "exits 0 with 8 assertion `OK` lines" is gone; the same line now reports the measured
   per-source assertion counts for round 33 (S049 `Q1`-`Q8`, S050 `Q1`-`Q6`). The line number is
   preserved as required by R6, so the round-31 spotcheck anchors still resolve.
3. **Reported, not smoothed (deviation from the item's literal expectation).** `anchorcheck.py
   SKILL.md` shows 12 in-range cites, not the 7 the round-31 text carried; the five extra anchors
   are the round-33 SKILL append's citations (`ExecRegressionC1.md` D-R33-1; corroborated by
   `ExecNoHarmFinal.md` §4). All failure classes are unchanged and the exit is 0.
4. **`SCORECARD.md` capability row is not cited and not verified by this seat.** `ScribeScorecard.md`
   had not landed at 04:46Z; the box-1 evidence therefore cites the SKILL registry row only.
   `ExecRegressionC1.md` D-R33-2 already routes the SCORECARD row to the L1.
5. **`ExecNoHarmFinal.md` landed mid-seat (first seen 01:46 local; final mtime 01:48:58).** It was absent when the evidence hunt
   began, so the density/anchor numbers were taken from `ExecRegressionC1.md`; the late receipt
   agrees on both numbers and explicitly places `SHONEN.md` outside its scope.
6. **Box 2 stays `[~]` by construction**: no round-33 `LOG.md` entry exists and `LOG.md` is the
   L1's path (`grep -c '^## Round 33' LOG.md` = 0). This seat did not write `LOG.md`.
7. **Not re-measured by this seat:** the instruments themselves (capture-binding-check,
   recheck-audit, source-recheck, frontier-recheck-count, density, anchorcheck) — their runs are
   cited from the executor receipts; only the digest/line-count identity checks in §4 were run here.

## 6. Artifact paths (lane-relative)

- `SHONEN.md` (edited, 42 lines, sha256 `a8d7d203…afdc008a`)
- `.ufo/waves/round-33/wave1/ScribeShonen.md` (this receipt)
- evidence: `.ufo/waves/round-33/wave1/{ExecRegressionC1.md,ExecNoHarmFinal.md,ExecExpectedList.md,ExecHarnessC2.md,ScribeSkillGate.md,ScribeProvince.md,ConnSibling.md}`
  and raws `.ufo/waves/round-33/wave1/ExecRegressionC1/`
