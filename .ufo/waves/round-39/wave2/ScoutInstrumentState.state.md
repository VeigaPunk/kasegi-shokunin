# ScoutInstrumentState — instrument inventory and gate status on the integrated tree (round 39, wave 2)

Seat: ScoutInstrumentState (scout, ATTACK posture; authored none of the work under test). Measured 2026-10-26 ~20:15-20:19Z.
Lane HEAD = `5006097a84305267c9a3e8c1e1d560e60fe41d37` (= Y, "round-39: receipt Y (all-gates v3)"); J = `46c66c268502abd1b2c342fc71bf88ccf721845b`
(`git diff --name-only J Y` = `.ufo/waves/round-39/final-gates/all-gates.txt` only). Base `480b1a50…`; r38 judged head `66703acaaff50529a35be49aa8759d04140720ad` (E2 40-char form).
Live lane worktree during the measurement: 5 untracked wave-2 paths (`kasegi-r39-falsify.ready*`, `wave2-dispatch.json`, `wave2-run.err`, `wave2/`), tracked tree clean. No lane file was written; every mutation/clone ran under `/fast/scratch/hyaku/kasegi-r39/ScoutInstrumentState/` (removed at exit).

## 1. Inventory — `corpus/instruments/` (tracked; `git ls-files`) with sha256[:12] and documentation coverage

| file | sha256[:12] | README hits | SKILL.md hits |
|---|---|---|---|
| anchorcheck.py | d0f35f8ccdcf | 15 | 4 |
| capture-binding-check.py | 3d9e5e0ddbaa | 10 | 6 |
| capture-source.py | e1831888d719 | 1 | 0 |
| citation-survival.md / .tsv | 795ba4f2801f / 793e0a4e456b | 3 / 1 | 2 / 0 |
| density.py | ee803726a322 | 4 | 0 |
| frontier-recheck-count.py | 1be79af60cb5 | 10 | 5 |
| kill-rule-check.py | c279d952cba5 | 5 | 3 |
| knowledge-expected.txt | 71282ee8a717 | 0 | 0 |
| limb-ledger.json / limb-mutation-check.py | c042adf6b25c / 237fd07cbcb4 | 9 / 10 | 3 / 3 |
| mirror-containment-check.py / -fixtures.json | dddd55496b55 / d05b1e0cf627 | 1 / 1 | 0 |
| r-defect-closure.sh | 809aaf9078a2 | 0 | 3 |
| r35-defect-closure.sh | 0ae4b4848b10 | 0 | 1 |
| r36-closure.sh | 4db1ae70c76a | 0 | 2 |
| r37-closure.sh | 0da98e37b5a8 | 0 | 1 |
| r38-closure.sh | 85d33ea9d386 | 0 | 1 |
| r39-closure.sh | 2856a210d783 (= `suite-sha256` in receipt) | 0 | 0 |
| recheck-audit.py | 5d4842da6103 | 6 | 5 |
| resolve.py / test_resolve.py | db5e0767c60c / 16a6ff281d89 | 12 / 1 | 2 / 0 |
| resolve-dispatch-check.py / -fixtures.json | acbb687094f0 / fef0f02d6d64 | 1 / 1 | 0 |
| score-gap.py | 57584fda83b8 | 9 | 2 |
| source-recheck.py | fd2e01e88c8c | 10 | 6 |
| (dirs) limb-fixtures/, r35-fixtures/ | — | — | — |

## 2. Gate/probe results on the integrated tree (cwd = lane root, rc = exit code; scratch-bound `TMPDIR`)

| instrument · command | rc | key output |
|---|---|---|
| `capture-binding-check.py` | 0 | `AUDIT records=46 … snapshot_dirs=15 manifest_dirs=15 missing_manifest=0 multi_row_url=2 orphans=1 orphan=S040-live.txt` / `records=46 bound=46 unbound=0` (C2 binding 46/46 holds) |
| `capture-binding-check.py --selftest` | 0 | `selftest cases=23 failures=0` |
| `frontier-recheck-count.py` | 0 | 25 PASS lines incl. `PASS F22 knowledge/cisa-when-to-issue-vex.md ids=S057 exit=0`; `entries=25 pass=25 exit=0` (C2 holds) |
| `frontier-recheck-count.py --selftest` | 0 | `selftest cases=6 failures=0` |
| `recheck-audit.py --quiet` | 0 | `strict pass=51/51 …`; `lines=51 total=51 pass=51 fail-closed=24 … exit=0`; `expect=present expected=51 missing=0 unexpected=0 exit=0` (C2 audit expected=51 holds) |
| `recheck-audit.py --selftest` | 0 | 39 lines, last = `selftest complete-missing-line … ok`; no failure line |
| `source-recheck.py --manifest …/round-39/manifest.json --source S057` | 0 | `S057:sha256 OK`, `Q1..Q4 OK … occurrences=1 anchor=12/132/136/184-ok` |
| `source-recheck.py` over ALL 15 `corpus/source-snapshots/round-*/manifest.json` | 0 each | every manifest rc 0 (round-23,24,25,26,28,29,30,31,32,34,35,36,37,38,39) |
| `source-recheck.py --selftest` | 0 | `selftest cases=10 failures=0` |
| `anchorcheck.py --selftest` | 0 | `selftest cases=12 failures=0`, `limbs=9 covered=9` |
| `anchorcheck.py` on SKILL.md / PROVINCE.md / corpus/README.md / corpus/SOURCES.md / knowledge/cisa-when-to-issue-vex.md | 0 | SKILL.md `in-range=16 bad=0 base-absent=0 exit=0` per `score-gap`; others `bad=0` |
| `anchorcheck.py corpus/lessons/round-39.md` | **1** | `BASE-ABSENT md:24 S057.txt:12-14 (base tree absent: /home/vgpnk/Projects/the-bounty-hunter/S057.txt)` — see D2 |
| `anchorcheck.py corpus/instruments/README.md` | 1 | 3 BASE-ABSENT carried since r17/r24; README flags itself (documented, README "This file is flagged by its own rule") |
| `density.py SKILL.md` | 0 | `Total path-citation instances: 768 across 27 blocks`, mean dens 233.1 |
| `density.py corpus/knowledge/cisa-when-to-issue-vex.md` | 0 | 0 path-citation instances across 17 blocks (entry cites by `source:`/capture id, not path:line; density is not an F22 gate) |
| `limb-mutation-check.py` (no args) | **2** | `--ledger is required` (usage, not a verdict — see §5 note) |
| `limb-mutation-check.py --ledger corpus/instruments/limb-ledger.json` | 0 | `limbs=13 killed=13 survivors=0`, `controls=3 rejected=3`, `guard cases=3 failures=0` |
| `limb-mutation-check.py --selftest` | 0 | `selftest cases=20 failures=0` |
| `kill-rule-check.py` | 0 | `mutants=3 killed=3 survivors=0 invalid=0`, `controls=4 rejected=4`, `gates=7 failed=0`, `survivors=0` |
| `kill-rule-check.py --selftest` | 0 | `selftest cases=3 failures=0` |
| `mirror-containment-check.py` | 0 | `cases=24 escape=12 controls=12 pass=24 fail=0` |
| `resolve-dispatch-check.py` | 0 | `cases=8 pass=8 exit=0` |
| `test_resolve.py` | 0 | `OK` |
| `capture-source.py --selftest` | 0 | `selftest normalize=ok deterministic=ok` |
| `score-gap.py` / `--selftest` | 0 / 0 | `gap: 24 of 51 rechecks still gated on a lost base`; `selftest fields=7 failures=0` |
| `r-defect-closure.sh` / `--selftest` | 0 / 0 | `closed=9/9 exit=0` / `selftest judge=complete-report accepted=1` |
| `r35-defect-closure.sh` / `--selftest` | 0 / 0 | `closed=7/7 exit=0` / `selftest judge=complete-report accepted=1` |
| `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` | 0 | only W04 S028 + S029 (byte-identical to `.ufo/waves/round-39/census-before.txt`; no new W/E code; C2 census clause holds) |

### r36–r39 closure suites (export mode)

Two environments matter, and the difference is itself a finding (D1 below): (A) the live lane worktree (5 untracked wave-2 paths, ~30 peer dirs under `/fast/scratch/hyaku/kasegi-r39/`), (B) a pristine `git clone` of the lane at HEAD=Y in my scratch (`--lane <clone> --scratch-root <empty>`, so G6/E9 see a quiescent host; prints `deviation=non-default --lane/--scratch-root`).

| command | (A) live lane | (B) clean clone, HEAD == ref |
|---|---|---|
| r39 `--export-ref Y` | rc 1: `closed=6/8` with the default scratch root (G6 `r39=present`, G8 `r37-closed=0`); `closed=7/8` with `--scratch-root <empty dir>` (only G8 red: r37 E9 `status-dirty=5`) | **rc 0 `closed=8/8 exit=0`** (G1–G8 all `closed=1`, G2 `graded-cases=8,ungraded-cases=0,closed-line=1,run-lines=8`, G8 `r37-closed=1,r37-exit=0`) |
| r39 `--selftest --export-ref Y` | rc 1 `selftest cases=8 failures=1` (only `G8 positive=fail`, same E9 cause) | **rc 0 `selftest cases=8 failures=0`**, case lines `G1 mutants=4/4, G2 8/8, G3 2/2, G4 6/6, G5 4/4, G6 4/4, G7 3/3, G8 3/3`, all `positive=pass … verdict=pass` |
| r39 `--export-ref J` | live lane (HEAD=Y): rc 1 `closed=6/8` (G2 + G8) | HEAD=J fixture: rc 1 `closed=7/8` (G2 `receipt=0,…`, other 7 closed) — matches erratum E4; `--selftest` there: `G2 positive=fail`, `selftest cases=8 failures=1`. Clone with HEAD=Y but ref J: `closed=6/8` (G2 + G8 head-match=0) |
| r39 `--export-ref 480b1a50…` (base) | rc 1 `closed=2/8` | rc 1 `closed=2/8` |
| r39 `--export-ref 66703aca…0ad` (r38 head) | rc 1 `closed=2/8` | rc 1 `closed=2/8` |
| r39 plain (no flag) | rc 2 `refusing to run against the live worktree` | rc 2 (same) |
| r38 `--export-ref Y` | rc 1 `closed=4/8` | rc 1 `closed=5/8` (G1 declared-blocks=0, G2 diff-clean=0, G3 added-pending=1 — r38 evidence checks are round-bound) |
| r38 `--export-ref 66703aca…` | rc 1 `closed=6/8` | rc 1 `closed=6/8` (G2 receipt=0 by construction, G8 r37 red) |
| r38 `--selftest --export-ref Y` (clone) / `--export-ref r38head` (live) | live r38head: rc 1 `selftest cases=8 failures=2` | clone at Y: rc 1 `selftest cases=8 failures=3` (G1/G2/G3 positives fail at a round-39 head; round-bound, historical) |
| r37 `--export-ref Y` | rc 1 `closed=13/14` (E9 `status-dirty=5`) | **rc 0 `closed=14/14 exit=0`** |
| r37 `--selftest --export-ref Y` | — | rc 0 `selftest cases=14 failures=0` |
| r36 `--export-ref Y` / `--selftest` | rc 1 `closed=8/9` (E9 `status-dirty=5`) | **rc 0 `closed=9/9 exit=0`** / rc 0 `selftest cases=9 failures=0` |

## 3. Frozen C1/C2 spot re-derivation (counting commands)

- C1: G1–G8 all close at Y in environment B; kill-rule reds hold (base 2/8, r38 head 2/8, plain exit 2); selftest 8 graded lines, none `mutants=0/0`, none with empty payload.
- C2 (E1 value 59 applies): `grep -cE '^\| F[0-9]+ \|' corpus/README.md` = 22 (base 21); registry rows = 59 (base 55; frozen 58 superseded by E1); `grep -rlE '^source: S057' corpus/knowledge | wc -l` = 1; `ls corpus/knowledge/*.md | wc -l` = 51; S057 row has 11 cells = `awk -F'|'` NF=13 like S050–S055 (checked by split), S056/S058/S059 rows present; entry 144 lines, `source: S057`, `recheck:` line present.
- C2 do-nothing control (`c2-controls/before.txt`): frontier 21, registry 55, harness `entries=24`, binding `records=45 bound=45`, audit `expected=50` — all differ from the after-values, so the counters discriminate.
- junk-f22 control replayed (fixture `c2-controls/junk-manifest.json` + real `S057.txt` in scratch): `S057:sha256 OK`, `S057:J1..J4 MISMATCH reason=quote-not-found`, rc 1 (junk rejected).
- Five one-limb mutations on a scratch clone, each restored after (lane untouched): drop `source: S057` header → `FAIL F22 … problems=no-source-line`, `entries=25 pass=24 exit=1`; alter S057 row URL → `FAIL rule=url-mismatch record=S057`, `records=46 bound=45 unbound=1`, rc 1; flip S057 row status to `rejected` → `FAIL rule=rejected-row-anchor record=S057`, rc 1; delete the F22 entry → harness `FAIL F22 … problems=missing-entry` AND audit `expected=51 missing=1 … exit=1`; append a byte to `S057.txt` → `S057:sha256 MISMATCH`, rc 1. Every limb is load-bearing.

## 4. Defects / hazards found (ranked)

- **D1 (reproduction hazard on the frozen C1 counting command; documented in `r39-closure.sh:185` and `ExecSuiteBuild.md:244`, but not stated in claims.json or E4).** `--export-ref Y` prints `closed=8/8` only when the lane's live HEAD equals `Y` exactly, the lane worktree is porcelain-clean, and no `kasegi-r37/r38` scratch exists and `kasegi-r39` holds only the run's own work dir: G8 executes the pinned r37 suite whose E9 reads live `status`/`HEAD`/scratch. Measured: live lane now → `closed=6/8` (G6 `r39=present`; G8 `r37-closed=0` via E9 `status-dirty=5`); clean clone at Y → 8/8; clean clone with ONE extra commit past Y (fixture commit `88962c7`, ref still Y) → `closed=7/8` with G8 `r37-closed=0,r37-exit=1`. Consequence: once the L1 commits wave-2/report evidence after Y, the verifier command at `<Y>` run in the lane goes 7/8; only a `--lane` clone checked out at Y reproduces 8/8. Not a defect in the closure semantics (E9 is fail-closed by design) but the filing and any non-author re-run must carry that precondition, and while any wave-2 seat holds a `kasegi-r39/<seat>` scratch dir, G6 cannot be green in the live lane by design (G6 is host-state).
- **D2 (minor, landed lesson).** `corpus/lessons/round-39.md:24` cites `S057.txt:12-14` as a bare name; `anchorcheck.py` resolves bare names against the mirror (absent) → `BASE-ABSENT`, exit 1, 1 instance. Same class pre-exists in `round-37.md` (5), `round-38.md` (9), `round-38-verifier-spotcheck.md` (2), so it follows precedent and no frozen gate reads it; the lane-prefixed form `corpus/source-snapshots/round-39/S057.txt:12-14` would be IN-RANGE.
- **D3 (stale census of record).** `corpus/instruments/citation-survival.md` was last regenerated in round-20 (`git log`: 644ed37); `score-gap.py` still reports its committed figures `census-lane: 134/1480 = 9.05%`, `census-skill: 32/506 = 6.32%`. A fresh `resolve.py <lane>` run in a scratch clone (committed files untouched) prints `distinct=3488 resolves=33 mirror=0 internal=671 other=0 gone=2784 skill=83/608 corpus=674/3120 all=704/3488` (lane 704/3488 = 20.18%, SKILL 83/608 = 13.65%). Not claim-bearing this round; the depth:verifiability gap report is reading a 19-round-old denominator.
- **D4 (docs coverage).** `r35-defect-closure.sh`, `r36`–`r39` suites and `r-defect-closure.sh` have 0 hits in `corpus/instruments/README.md`; `r39-closure.sh` has 0 hits in SKILL.md too (r35–r38 have 1–3). `knowledge-expected.txt` has 0 hits in either (it is described in the recheck-audit docstring).
- **D5 (cosmetic noise).** r39 G6's `g6_chain_ok` runs `cd "$e"` on every entry under a tolerated parent; a plain file next to the work dir (e.g. outputs in the same scratch dir as `--work`) prints `r39-closure.sh: line 555: cd: <file>: Not a directory` to stderr per entry, while G6 stays RED/fail-closed — verdict correct, message noisy (reproduced with TMPDIR set to a dir holding `.out`/`.rc` files; `closed=5/8`).
- No instrument fails on the landed tree in environment B. In environment A the only reds are D1's host-state limbs (r37/r38/r39 suites) and the two known historical-state items (r38 selftest at a round-39 head; README/own BASE-ABSENT).

## 5. Notes
- `limb-mutation-check.py` with no args exits 2 (`--ledger is required`); the documented entry is `--ledger corpus/instruments/limb-ledger.json` (README:349), which exits 0. Not a defect.
- `recheck-audit.py --expect` takes a PATH (expected list), not a count; my first invocation `--expect 51` printed `expect=absent` and was discarded; the frozen counting command `recheck-audit.py --quiet` (default `corpus/instruments/knowledge-expected.txt`, 53 lines = 2 header + 51 entries) prints `expected=51`.
- No tool installs, no network fetches this seat.
