# ExecC1BaseFail — r36-base red baseline for the r36 closure counter

Round 37, claim C1 (`depth:verifiability`), seat ExecC1BaseFail (leaf executor; no subagents, one read-only probe budget unused).
Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (the only repo written; this receipt + scratch only).
Lane HEAD at run time: `b362068195d5489aa94b31e6ec8f880c367e0ba0` (round-37 wave in flight; 6 untracked round-37 wave entries).
Instrument: `corpus/instruments/r36-closure.sh`, sha256 `4db1ae70c76afd28b29e9ec24c2e44835322c61fa33e30c966f75ce0dfadb7c4`, 894 lines, tracked since `caa3146`.

**Verdict: the frozen r36-base negative expectation holds.**
`bash corpus/instruments/r36-closure.sh --export-ref cc692008b0cfd58d18275aa6c4aed79620120799` → **`closed=4/9 exit=1`** (open: E1, E3, E4, E8, E9; closed: E2, E5, E6, E7), i.e. `closed<9/9 exit=1`.
Same suite on the r36 judged head `a23dc478…` reads `closed=8/9 exit=1` with **only the live E9 limb open** — so the r36 base's four extra reds are the round-36 landing delta, not harness noise.

## 1. Instrument and interface actually exercised

| field | value |
|---|---|
| path executed | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r36-closure.sh` (lane worktree copy; `git diff --quiet HEAD -- <path>` → clean, so the worktree bytes are the committed `caa3146` bytes) |
| sha256 | `4db1ae70c76afd28b29e9ec24c2e44835322c61fa33e30c966f75ce0dfadb7c4` — identical to the copy inside the r36 judged-head export (`a23dc478…/corpus/instruments/r36-closure.sh`), and the header of every run prints the same `suite-sha256=` |
| present at r36 base? | **no** — `git ls-tree -r --name-only cc692008… -- corpus/instruments/r36-closure.sh` = 0 lines; the export's `corpus/instruments/` holds `r35-defect-closure.sh`, `r35-fixtures/`, `r-defect-closure.sh` but neither `r36-closure.sh` nor `r36-fixtures/` |
| present at r36 judged head? | yes (1 line in `ls-tree`, copy sha identical) |
| run mode | export mode only (`--export-ref`); the suite refuses a plain run with exit 2 by construction, so no worktree-reading mode exists to abuse |
| decl. limits carried by the suite | E9 is live by definition (worktree status, scratch root, HEAD); historical exports can only read "not quiescent now", which is the intended meaning of the negative control |

Refs and trees used:

| ref | role | commit | tree |
|---|---|---|---|
| `cc692008…` | r36 base (= tip of the round-35 integration; subject `round-30: hyaku run-8 orchestrator salvage …`, committed 2026-10-26T09:05:45-0300) | `cc692008b0cfd58d18275aa6c4aed79620120799` | `c6f1dbec5c8763fbe368abda6d1e575008ff235c` |
| `a23dc478…` | r36 judged head (cross-check) | `a23dc4788aa7c98831eed6db953434034ce5ae8d` | `78f74821afb6d22479d3c3bdefb27a6c6e270709` |
| `b362068…` | lane HEAD during all runs (round-37, not an export ref here) | `b362068195d5489aa94b31e6ec8f880c367e0ba0` | — |

`git merge-base cc692008… HEAD` = `cc692008…` (base is an ancestor of the live head); `git log --oneline cc692008..HEAD` = 16 commits, round 36 starting at `b47f2cd`.

## 2. Command 1 — r36 suite over the r36 base export

Canonical form, run from the lane root, scratch bound through `TMPDIR` (nothing in an inherited temp dir), 2026-10-26:

```bash
S=/fast/scratch/hyaku/kasegi-r37/ExecC1BaseFail
TMPDIR="$S/tmp" bash corpus/instruments/r36-closure.sh --export-ref cc692008b0cfd58d18275aa6c4aed79620120799
```

stdout verbatim, **exit code 1**, stderr empty (sha256 of transcript `4f996bb93012100f5f37680da589a76428ff0f9601f07ce0f8633f9acfb18f89`):

```
export-ref=cc692008b0cfd58d18275aa6c4aed79620120799 mode=export lane=/home/vgpnk/Projects/shokunin/kasegi-shokunin suite-sha256=4db1ae70c76afd28b29e9ec24c2e44835322c61fa33e30c966f75ce0dfadb7c4
E1 payload=placeholders=0,lane-hash-markers=0,round36-section=0,round36-final-lane-commits=0,bound=0 closed=0
E2 payload=erratum-marker=1,erratum-row=1,erratum-mean=6 closed=1
E3 payload=registry-r35-defect-closure=0,registry-r36-closure=0 closed=0
E4 payload=tracked-ref=1,tracked-index=1,provenance-note=0 closed=0
E5 payload=claims-erratum-d5=1 closed=1
E6 payload=path=.ufo/waves/round-34/wave1/L1Integration.md,correction-round35=1 closed=1
E7 payload=supersedes-r22=1,supersedes-r23=1 closed=1
E8 payload=m36-rows=0,names-corrected-line=0,stale-line=0,round35-lesson=1 closed=0
E9 payload=status-dirty=6,scratch-seat-dirs=0,head-match=0,lane-root=1,scratch-root=present closed=0
closed=4/9 exit=1
```

Reproduction with explicit ownership of every write path (`--work` and `--scratch-root` inside my scratch, `2026-10-26`) — identical verdict, header adds `deviation=non-default --scratch-root`; transcript sha256 `56d822645d95334feab59536e3c6e0bf713c0dbb67b80a433585721043123f3e`:

```
export-ref=cc692008b0cfd58d18275aa6c4aed79620120799 mode=export lane=/home/vgpnk/Projects/shokunin/kasegi-shokunin suite-sha256=4db1ae70c76afd28b29e9ec24c2e44835322c61fa33e30c966f75ce0dfadb7c4
deviation=non-default --scratch-root
E1 payload=placeholders=0,lane-hash-markers=0,round36-section=0,round36-final-lane-commits=0,bound=0 closed=0
E2 payload=erratum-marker=1,erratum-row=1,erratum-mean=6 closed=1
E3 payload=registry-r35-defect-closure=0,registry-r36-closure=0 closed=0
E4 payload=tracked-ref=1,tracked-index=1,provenance-note=0 closed=0
E5 payload=claims-erratum-d5=1 closed=1
E6 payload=path=.ufo/waves/round-34/wave1/L1Integration.md,correction-round35=1 closed=1
E7 payload=supersedes-r22=1,supersedes-r23=1 closed=1
E8 payload=m36-rows=0,names-corrected-line=0,stale-line=0,round35-lesson=1 closed=0
E9 payload=status-dirty=6,scratch-seat-dirs=0,head-match=0,lane-root=1,scratch-root=present closed=0
closed=4/9 exit=1
```

Check-count arithmetic: payload `closed=1` fields are E2/E5/E6/E7 → 4; the printed `closed=4/9` matches the field count, so the summary is not a canned string. Both runs are byte-identical apart from the `deviation=` line; `--work` dirs are empty afterwards (the suite removes its extraction), `scratch2/` and `tmp/` are empty.

### 2a. Which E1–E9 are open at the r36 base, and why (independent reads on the export)

| check | state | cause (verified against `$S/r36base`, the export root) |
|---|---|---|
| E1 | **OPEN** (`round36-section=0`) | `grep -n '^#\{1,4\} .*Round[- ]\?36' SCORECARD.md` → exit 1: the base carries Round 31/33/34/35 sections and no round-36 block, so the scoped `Final lane commit:` hash clause has nothing to bind (`bound=0`). Both placeholder spellings are already 0 (`placeholders=0, lane-hash-markers=0`). |
| E2 | closed | `SCORECARD.md:1246` `Erratum (round 35): … mean 201.2 …`; erratum anchor ≥ 1, corrected mean present 6×; depth:density row at `:1269` reads `mean ≈ 201.2`. |
| E3 | **OPEN** (`0 / 0`) | Gates & probes registry at base `SKILL.md:977–982` holds only `recheck-audit.py` and `anchorcheck.py`; `grep -n 'r36-closure\|r35-defect-closure' SKILL.md` → exit 1 (no mention at all, row or prose). |
| E4 | **OPEN** (`provenance-note=0`) | `.ufo/waves/round-35/wave1-results.json` is tracked at the ref and in the live index (`1/1`), but `.ufo/waves/round-35/wave1-results.json.provenance.md` does not exist in the export (`ls` exit 2; only `wave1-results.json`, 301842 bytes, and `claims-erratum-d5.md`, 13086 bytes). |
| E5 | closed | `.ufo/waves/round-35/claims-erratum-d5.md` present in the export (13086 bytes). |
| E6 | closed | `.ufo/waves/round-34/wave1/L1Integration.md:34` `- Correction (round 35): the bullet above was corrected in place …`. |
| E7 | closed | `corpus/QUALITY.md:249` row whose third column begins `supersedes R22`, `:250` same for `supersedes R23`. |
| E8 | **OPEN** (`m36-rows=0, names-corrected-line=0`) | `corpus/lessons/round-36.md` absent in the export (`ls` exit 2); only `corpus/lessons/round-35.md` exists. `stale-line=0` because the false `source-recheck exit 0 on committed bytes` line is itself a round-36 addition, not base bytes. |
| E9 | **OPEN** (`status-dirty=6, head-match=0`) | Live limbs: the lane worktree had 6 untracked round-37 wave entries at run time (`git status --porcelain`: `.ufo/waves/round-37/assimilation/`, `wave1-plan.err`, `wave1-run.err`, `wave1.ready`, `wave1.ready.partial`, `wave1/`), and the export ref `cc692008…` is not lane `HEAD` `b362068…`. `scratch-seat-dirs=0` (default root `/fast/scratch/hyaku/kasegi-r36` exists and is empty), `lane-root=1`. |

## 3. Command 2 — `r37-closure.sh` is absent at the r36 base (and at the live lane head)

```bash
cd $S/r36base && ls corpus/instruments/r37-closure.sh   # → exit 2 (No such file or directory)
ls /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r37-closure.sh  # → exit 2
```

Both the r36-base export and the live lane worktree (`b362068…`) lack `corpus/instruments/r37-closure.sh`, and `git ls-files` finds no tracked copy. **Consequence for this seat's scope:** the round-37 14-check suite cannot be executed by me, because it does not exist in the lane yet (it is the artefact the suite-building seat lands). The baseline I can and do deliver is the r36 instrument's red at the r36 base, which is the lower control the frozen C1 claim's descent (r36 base → r36 judged head → r37 head) rests on.

## 4. Command 3 — D1–D6 defect-state greps at the r36 base (with the judged head as the defect-present side)

Measured on the freshly extracted exports (`$S/r36base`, `$S/r36judged`), 2026-10-26:

| probe | r36 base `cc692008` | r36 judged head `a23dc478` | reading |
|---|---|---|---|
| D1 — round-37 final-gates output | `find … -path './.ufo/waves/round-37/final-gates/all-gates.txt'` → no output; `ls .ufo/waves/round-37` → exit 2 (the whole round-37 dir is absent) | same: `ls .ufo/waves/round-37/final-gates/all-gates.txt` → exit 2 | E10's input file exists nowhere yet; D1 state is "no digest-header artifact at all", so E10 is open at both refs by construction |
| D2 — false fixture path in the round-36 C1 bullet | `grep -cF 'r36-fixtures' LOG.md` → **0**, exit 1 | `grep -cF 'r36-fixtures' LOG.md` → **1**, `LOG.md:1665`: ``Landed `corpus/instruments/r36-closure.sh` + `corpus/instruments/r36-fixtures/`.`` while `ls corpus/instruments/r36-fixtures` → exit 2 (`find -name 'r36-fixtures*'` → nothing; the only fixture dir is `r35-fixtures/`) | D2 (a named false path) is introduced by round 36; the base cannot carry it |
| D4 — stale final-lane label | `grep -c 'Final lane commit: e666d902' SCORECARD.md` → **0**, exit 1 (base `grep -n 'Final lane commit'` shows only the round-33/34 lines at `:987`, `:1129`) | → **1**, `SCORECARD.md:1492` `Final lane commit: e666d902337a49dcbfc77880939874f39c6f477b` | D4 is a round-36 artefact; present at the judged head only |
| D5 — SKILL registry row type cell | no `r36-closure.sh` row at all (`grep -n 'r36-closure' SKILL.md` → exit 1); base registry rows (`:981`, `:982`) use an unescaped literal `gate\|probe` cell | `SKILL.md:1111` `\| r36-closure.sh \| gate\\\|probe \| …` — the type cell is still a literal `gate\|probe` choice-list, and the verdict-map cell is ``one `E<n> payload=… closed=0\|1` line per check E1–E9, then `closed=K/9 exit=0\|1`; exit 0 only for K=9`` with **no** `exit 2 -> could-not-evaluate` mapping (`grep -c 'could-not-evaluate' SKILL.md` = 1 elsewhere in the file; the r36 row itself matches 0) | E13's two limbs are both open at the judged head; at the base the row is simply absent |
| D6 — fail-open quiescence shape | executed suite line 466 `porcelain=${porcelain:-0}`; `grep -cF 'porcelain:-0' corpus/instruments/r36-closure.sh` on the **executed** copy → **1** (export copy is absent, grep exit 2) | same → **1** (line 466; copy sha identical) | E14's fail-closed shape is not met by the r36 instrument: line 465 pipes `git --no-optional-locks … status --porcelain 2>/dev/null \| count_lines` and line 466 defaults an empty read to 0, so an unreadable status reads clean |

**Correction to the item's stated base expectations.** The item predicted `grep -cF 'r36-fixtures' LOG.md` "context" and `grep -c 'Final lane commit: e666d902' SCORECARD.md` **≥1** at the r36 base. Measured: **0 and 0** at the base, **1 and 1** at the r36 judged head. Both strings are round-36 additions (`caa3146`/`2c26a97`), so they cannot appear in the round-36 base tree; the defect-present side of D2/D4 is the judged head, not the base. I report the measured values rather than the prediction.

## 5. Cross-check — same suite over the r36 judged head (upper control)

```bash
bash corpus/instruments/r36-closure.sh --export-ref a23dc4788aa7c98831eed6db953434034ce5ae8d --work "$S/work3" --scratch-root "$S/scratch3"
```

stdout verbatim, **exit code 1**, stderr empty (transcript sha256 `bb66b201d68aa054b008249ccb867bfcb20f80417159764143d47347df01b07f`):

```
export-ref=a23dc4788aa7c98831eed6db953434034ce5ae8d mode=export lane=/home/vgpnk/Projects/shokunin/kasegi-shokunin suite-sha256=4db1ae70c76afd28b29e9ec24c2e44835322c61fa33e30c966f75ce0dfadb7c4
deviation=non-default --scratch-root
E1 payload=placeholders=0,lane-hash-markers=0,round36-section=1,round36-final-lane-commits=2,bound=2 closed=1
E2 payload=erratum-marker=1,erratum-row=1,erratum-mean=7 closed=1
E3 payload=registry-r35-defect-closure=1,registry-r36-closure=1 closed=1
E4 payload=tracked-ref=1,tracked-index=1,provenance-note=1 closed=1
E5 payload=claims-erratum-d5=1 closed=1
E6 payload=path=.ufo/waves/round-34/wave1/L1Integration.md,correction-round35=1 closed=1
E7 payload=supersedes-r22=1,supersedes-r23=1 closed=1
E8 payload=m36-rows=4,names-corrected-line=3,stale-line=0,round35-lesson=1 closed=1
E9 payload=status-dirty=6,scratch-seat-dirs=0,head-match=0,lane-root=1,scratch-root=present closed=0
closed=8/9 exit=1
```

`8/9`: only the live E9 limb is open (historical export ≠ live `HEAD`; the worktree carries the round-37 wave's untracked entries). The four r36-base reds E1/E3/E4/E8 are green here, which is the exact discrimination the negative control needs: the base red is a landing delta, not an artefact of how the suite is invoked. E1 now reads `round36-section=1, round36-final-lane-commits=2, bound=2` — two 40-hex values on/after a `Final lane commit:` line inside the round-36 block, both resolving and both ancestors of the exported ref.

## 6. Scope, side effects, tooling

- **Writes:** this receipt (written last) and scratch only — `/fast/scratch/hyaku/kasegi-r37/ExecC1BaseFail/` (two exports, three stdout transcripts, empty `tmp/`, `work2/`, `work3/`, `scratch2/`, `scratch3/`). Scratch removed at yield.
- **Read-only on the lane:** no file in the lane repo, fleet repo, sibling lanes or source trees was modified; no mutating git command was run (only `archive`, `rev-parse`, `log`, `merge-base`, `ls-tree`, `ls-files`, `status`, `diff`). The suite itself writes only under its `--work`/`TMPDIR` dirs and reads status with `--no-optional-locks`, so no `.git/index.lock` is taken.
- **Lane state before/after:** identical 6 untracked round-37 wave entries, 0 modified tracked files; the untracked `corpus/instruments/r36-closure.sh` does not exist (it is committed since `caa3146`).
- **Tooling:** no installs or upgrades (bash 5.3.20, git 2.56.0, GNU tar 1.35, coreutils sha256sum 0.8.0). `pacman` untouched.
- **Blocker for the 14-check limb (not for this seat):** `corpus/instruments/r37-closure.sh` is absent at both the r36 base and the live lane head `b362068…`; the round-37 `closed<14/14 exit=1` red on the r36 base can only be produced after the suite-building seat lands the r37 instrument. My measured r36-instrument baseline (`closed=4/9 exit=1` at `cc692008`) and its judged-head upper control (`closed=8/9 exit=1`, live E9 only) are the red/green pair this seat can supply.
