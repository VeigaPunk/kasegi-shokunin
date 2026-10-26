# ExecC1Fixtures — discriminating fixtures for the round-37 closure suite (E1–E14)

seat: `ExecC1Fixtures` (executor, leaf). Lane `kasegi-shokunin`, base `b56a41680cefd391868c1c370dc063c69d827e7d`,
claims freeze `224df74db2a46d627ae1475a72ca48796bbd177c`. Claim under work: **C1 depth:verifiability (score 4, held)**.

Job: for each check E1–E14 of the frozen C1 contract, one **minimal fixture that reopens exactly one clause**
and must be REJECTED, plus the payload/verdict that rejection prints. Fixtures are machine-generated scratch
trees; nothing was written under the lane except this receipt. All scratch lived under
`/fast/scratch/hyaku/kasegi-r37/ExecC1Fixtures` and was removed before yield; every output quoted here is the
instrument's own stdout, copied verbatim.

Tooling: **no installs, no upgrades, no pacman**. Git use is read-only (`archive`, `rev-parse`, `cat-file`,
`ls-tree`, `ls-files`, `status`) except `git init/add/commit` inside `mktemp -d` fixture repos whose
`rev-parse --show-toplevel` was compared to the fixture dir's `pwd -P` before any commit (guard present in
`build_git`, fatal on mismatch; it never fired).

## 0. What is executable at this seat's read, and what each fixture was run against

`corpus/instruments/r37-closure.sh` **does not exist** at this seat's read (`ls` exit 2, working tree
`b362068`). So the fixtures are executed against two discriminators, and every claim below names which one
produced the line:

| discriminator | bytes | how it was run |
|---|---|---|
| **the inherited suite** `corpus/instruments/r36-closure.sh` | sha256 `4db1ae70c76afd28b29e9ec24c2e44835322c61fa33e30c966f75ce0dfadb7c4` (894 lines; digest printed in its own run header) | `bash r36-closure.sh --lane <fixture-repo> --export-ref HEAD --work <scratch>/work/<name> --scratch-root <empty scratch dir>` — the suite archives the fixture repo and reads only the export |
| **E1 Round-37-scope variant** (scratch copy) | sha256 `d4b2c618cbe0a1a756468513f4fb09d8dd34b1f2f1ab8a21af62c3d08ed1ae05` | same, on a `sed 's/Round\[- \]?36/Round[- ]?37/g'` copy — **only** the round literal of E1's two awk scopes changed, so the same five limbs are shown against the heading the r37 suite will use |
| **stand-in for the new checks** (scratch) | sha256 `2d5c9191cae6f4e252a21efb5811bdaf30fcb51a697171a17fce416be0de21fe` | `bash standin.sh E10|E11|E12|E13|E14 <tree>` and `standin.sh E9FC <repo> <head> <scratch-root>`; implements the frozen claim's E10–E14 semantics verbatim and prints one `E<n> payload=… closed=0|1` line |

The stand-in is **not** the r37 instrument: it exists to prove each E10–E14 fixture reopens exactly one clause,
and to fix the expected payload substrings the real suite's `--selftest` `st_neg` needles should use (§5).

## 1. Green base fixture — the positive control every mutant is one edit away from

Synthetic lane tree (`write_tree` in the scratch builder), committed in a `mktemp -d` fixture repo with two
commits (`c1` = base, `c2` = the token fill that names `c1`; export ref = `HEAD` = `c2`). Content:

```markdown
# SCORECARD (fixture tree)

## Round 36 — fixture historical (2026-10-26)

Final lane commit: <C1>

Measured at the fixture head.

Frozen claims for the fixture tree follow.

## Round 37 — frozen claims C1/C2 (fixture)

Anchor ancestor (round-36 lane head): `c20300df516eb5575d8db2aaad1f0cf4913e7981`

Frozen claims for the fixture tree.

Final lane commit: <C1>

Erratum (round 35): the round-34 depth:density row is corrected below.

| depth:density | 9 | mean **201.2**, 25 blocks |
```

```markdown
# SKILL (fixture tree)

## Gates & probes registry

| name | type | entry command | verdict map | self-test | pinned-value path | write scope | owner |
|---|---|---|---|---|---|---|---|
| r35-defect-closure.sh | gate | bash corpus/instruments/r35-defect-closure.sh | exit 0 closed; exit 1 open; exit 2 -> could-not-evaluate | bash corpus/instruments/r35-defect-closure.sh --selftest | base export -> closed=0/7 exit=1 | read-only | kasegi |
| r36-closure.sh | gate | bash corpus/instruments/r36-closure.sh --export-ref <hash> | exit 0 closed; exit 1 open; exit 2 -> could-not-evaluate | bash corpus/instruments/r36-closure.sh --selftest | r35 base -> closed=0/9 exit=1 | read-only | kasegi |
```

```markdown
# LOG (fixture tree)

## Round 36 — fixture (2026-10-26)

- **C1 depth:verifiability (4 held).** Landed `corpus/instruments/r36-closure.sh` + `corpus/instruments/r36-fixtures/`. Export-mode suite over a named lane head.

## Round 37 — fixture (2026-10-26)

- **Correction (round 36 C1 bullet).** The round-36 C1 bullet names `corpus/instruments/r36-fixtures/`, which never existed at any head; corrected: the suite ships no fixtures directory.
- **C1.** Round-37 closure suite over exports.
```

`corpus/lessons/round-37.md` (E12 lesson limb):

```markdown
# Round 37 — fixture lesson

Anchor ancestry: the round-36 lane head `c20300df516eb5575d8db2aaad1f0cf4913e7981` is the `anchor ancestor`, not the round-37 final commit.

## Mistakes

| id | axis | mistake | control |
|---|---|---|---|
| M37-1 | landing | fixture row | fixture control |
```

`corpus/lessons/round-36.md` (E8): a row `| M36-2 | stale-premise | the round-35 lesson line "source-recheck exit 0
on committed bytes" is false at the judged head | E8 correction recorded here; source-recheck re-run on committed
bytes |`.
`corpus/lessons/round-35.md` (E8 absence limb): `Clean lesson: no stale evidence line retained.`
`corpus/QUALITY.md` (E7): `| R26 | a fixture criterion | supersedes R22 — fixture supersession row | x |` and
`| R27 | another fixture criterion | supersedes R23 — fixture supersession row | y |`.
E4/E5/E6 inputs: `.ufo/waves/round-35/wave1-results.json` = `{"wave": 1}`,
`.ufo/waves/round-35/wave1-results.json.provenance.md` (non-empty note),
`.ufo/waves/round-35/claims-erratum-d5.md`, `.ufo/waves/round-34/wave1/L1Integration.md` =
`Correction (round 35): appended by the round-35 closure.`
E10 inputs: `corpus/instruments/r37-closure.sh` fixture bytes (sha256 `63895fa4…c53acc1d`) and
`.ufo/waves/round-37/final-gates/all-gates.txt` with header `suite-sha256=<that sha>`, 14 `E<n> payload=` lines,
`closed=14/14 exit=0`, 14 `selftest case=E<n> …` lines, `selftest cases=14 failures=0`.

Positive-control output (r36 suite, export mode, harness bytes `4db1ae70…`):

```
export-ref=5425cacf7baecd1451bc90a4194f8bb8909fa96f mode=export lane=…/fx/green.m1ixDR suite-sha256=4db1ae70c76afd28b29e9ec24c2e44835322c61fa33e30c966f75ce0dfadb7c4
deviation=non-default --lane
deviation=non-default --scratch-root
E1 payload=placeholders=0,lane-hash-markers=0,round36-section=1,round36-final-lane-commits=1,bound=1 closed=1
E2 payload=erratum-marker=1,erratum-row=1,erratum-mean=1 closed=1
E3 payload=registry-r35-defect-closure=1,registry-r36-closure=1 closed=1
E4 payload=tracked-ref=1,tracked-index=1,provenance-note=1 closed=1
E5 payload=claims-erratum-d5=1 closed=1
E6 payload=path=.ufo/waves/round-34/wave1/L1Integration.md,correction-round35=1 closed=1
E7 payload=supersedes-r22=1,supersedes-r23=1 closed=1
E8 payload=m36-rows=1,names-corrected-line=1,stale-line=0,round35-lesson=1 closed=1
E9 payload=status-dirty=0,scratch-seat-dirs=0,head-match=1,lane-root=1,scratch-root=present closed=1
closed=9/9 exit=0
```

The same tree through the Round-37-scope E1 variant: `E1 payload=placeholders=0,lane-hash-markers=0,round36-section=1,
round36-final-lane-commits=1,bound=1 closed=1` … `closed=9/9 exit=0` (variant bytes `d4b2c618…`). Stand-in green:
`E10 closed=1`, `E11 closed=1`, `E12 closed=1`, `E13 closed=1`, `E14 closed=1`, and `E9FC` on the clean fixture repo
`E9 payload=status-read=ok,status-dirty=0,scratch-seat-dirs=0,head-match=1 closed=1`.

## 2. Per-check fixture → clause → rejection (the deliverable)

Each row is the green base **plus exactly one edit**; the observed line is the red check's own payload. Unless
noted, every other check in that run stayed `closed=1` and the suite ended `closed=8/9 exit=1`.

| check | clause reopened (one) | fixture edit (green base +) | expected needle | observed payload |
|---|---|---|---|---|
| E1 (a) | commit binding: every 40-hex on/after `Final lane commit:` resolves and is an ancestor | Round-36 block carries no binding; Round-37 `Final lane commit:` names `0123456789abcdef0123456789abcdef01234567` (absent from the fixture repo) | `bound=0` | `E1 payload=placeholders=0,lane-hash-markers=0,round36-section=1,round36-final-lane-commits=1,bound=0 closed=0` |
| E1 (b) | no L1 placeholder left in SCORECARD | append a line `filled by the L1` | `placeholders=1` | `E1 payload=placeholders=1,lane-hash-markers=0,round36-section=1,round36-final-lane-commits=1,bound=1 closed=0` |
| E2 | the round-34 depth:density **row** exists (prose quoting `201.2` does not stand in) | replace the table row with `Erratum (round 35): the round-34 depth:density row was corrected; guard mean 201.2.` | `erratum-row=0` | `E2 payload=erratum-marker=1,erratum-row=0,erratum-mean=1 closed=0` |
| E3 | the exact-basename row lives **inside** a `## …Gates & probes registry…` section | keep the `r35-defect-closure.sh` row; move the `r36-closure.sh` row into a following `## Cited paths` section | `registry-r36-closure=0` | `E3 payload=registry-r35-defect-closure=1,registry-r36-closure=0 closed=0` |
| E4 | the beside-provenance note exists | delete `.ufo/waves/round-35/wave1-results.json.provenance.md` (json stays tracked) | `provenance-note=0` | `E4 payload=tracked-ref=1,tracked-index=1,provenance-note=0 closed=0` |
| E5 | `claims-erratum-d5.md` present at the export | delete `.ufo/waves/round-35/claims-erratum-d5.md` | `claims-erratum-d5=0` | `E5 payload=claims-erratum-d5=0 closed=0` |
| E6 | the round-34 receipt carries **`Correction (round 35)`** | receipt body replaced by `Correction (round 34) only.` (path still derived from `ls-tree`, one candidate) | `correction-round35=0` | `E6 payload=path=.ufo/waves/round-34/wave1/L1Integration.md,correction-round35=0 closed=0` |
| E7 | the supersession is a **row** whose 3rd column begins `supersedes R23` | keep the R26 row; replace R27's row with prose `Note: R27's row supersedes R23 in spirit, recorded as prose only.` | `supersedes-r23=0` | `E7 payload=supersedes-r22=1,supersedes-r23=0 closed=0` |
| E8 (a) | the false-evidence line is gone from the round-35 lesson | put `Gate: source-recheck exit 0 on committed bytes.` back into `corpus/lessons/round-35.md` (round-36 lesson keeps its `M36` rows) | `stale-line=1` | `E8 payload=m36-rows=1,names-corrected-line=1,stale-line=1,round35-lesson=1 closed=0` |
| E8 (b) | the correction **names** the corrected instrument | round-36 lesson keeps an `M36` row but never says `source-recheck` | `names-corrected-line=0` | `E8 payload=m36-rows=1,names-corrected-line=0,stale-line=0,round35-lesson=1 closed=0` |
| E9 (a) | the worktree is clean | after `c2`, create untracked `dirty.txt` (export unchanged) | `status-dirty=1` | `E9 payload=status-dirty=1,scratch-seat-dirs=0,head-match=1,lane-root=1,scratch-root=present closed=0` |
| E9 (b) | **status read fails ⇒ red, never clean** | after `c2`, corrupt the index (`printf 'CORRUPT-INDEX' > .git/index`) | `status-read=failed` | stand-in: `E9 payload=status-read=failed,status-dirty=0,scratch-seat-dirs=0,head-match=1 closed=0` |
| E10 (a) | the gate transcript is bound to the suite bytes it claims | rewrite the header's 64-hex to `deadbeef…` (64 hex) | `digest-match=0` | `E10 payload=all-gates=1,suite-sha256=deadbeef…deadbeef,digest-match=0,payload-lines=14,payload-ids=14,closed-line=1,selftest-cases=14,selftest-ids=14,selftest-summary=1 closed=0` |
| E10 (b) | fourteen per-check payload lines | delete the `E14 payload=` line | `payload-lines=13` | `E10 payload=all-gates=1,suite-sha256=63895fa43438de759cff9f5c6037ec6dc2f5561201815c39c85caff9c53acc1d,digest-match=1,payload-lines=13,payload-ids=13,closed-line=1,selftest-cases=14,selftest-ids=14,selftest-summary=1 closed=0` |
| E11 (a) | the round-37 entry names the false `corpus/instruments/r36-fixtures/` path | drop the correction bullet; the path survives only in the round-36 section | `names-false-path=0` | `E11 payload=round37-entry=1,names-false-path=0,named-correction=0 closed=0` |
| E11 (b) | it is a **named correction**, not a mention | round-37 entry says only `The path corpus/instruments/r36-fixtures/ is mentioned in this entry.` | `named-correction=0` | `E11 payload=round37-entry=1,names-false-path=1,named-correction=0 closed=0` |
| E12 (a) | the stale label is absent **inside** the round-37 section | append `Final lane commit: e666d902337a49dcbfc77880939874f39c6f477b` to the round-37 section (the round-36 section may still carry it) | `stale-e666d902-label=1` | `E12 payload=round37-section=1,anchor-ancestor-label=1,stale-e666d902-label=1,lesson-anchor-ancestor=1 closed=0` |
| E12 (b) | `c20300df…` is labelled `anchor ancestor` | rewrite the anchor line as `Final lane commit: c20300df516eb5575d8db2aaad1f0cf4913e7981` | `anchor-ancestor-label=0` | `E12 payload=round37-section=1,anchor-ancestor-label=0,stale-e666d902-label=0,lesson-anchor-ancestor=1 closed=0` |
| E13 (a) | the `r36-closure.sh` row's type cell is a **single choice** | type cell `gate\|probe` | `type-single=0` | `E13 payload=registry-row=1,type-cell=[gate\|probe],type-single=0,verdict-exit2-could-not-evaluate=1 closed=0` |
| E13 (b) | the verdict map covers exit `2` → `could-not-evaluate` | verdict cell `exit 0 closed; exit 1 open` | `verdict-exit2-could-not-evaluate=0` | `E13 payload=registry-row=1,type-cell=[gate],type-single=1,verdict-exit2-could-not-evaluate=0 closed=0` |
| E14 (a) | no `${porcelain:-0}` default (status-read failure must not read 0) | append `porcelain=${porcelain:-0}` to the fixture suite source | `porcelain-default=1` | `E14 payload=suite-present=1,porcelain-default=1,status-swallow=0 closed=0` |
| E14 (b) | no `2>/dev/null` swallow on the status read | append `porcelain=$(git --no-optional-locks -C "$srepo" status --porcelain 2>/dev/null \| count_lines)` | `status-swallow=1` | `E14 payload=suite-present=1,porcelain-default=0,status-swallow=1 closed=0` |
| E14 (+) | the check is satisfiable by a fail-closed shape | suite source: `if ! porcelain=$(git --no-optional-locks -C "$srepo" status --porcelain); then printf 'status-read=failed\n'; return 1; fi` | `closed=1` | `E14 payload=suite-present=1,porcelain-default=0,status-swallow=0 closed=1` |

Two fixture runs carry extra weight:

**E1 scope transfer.** The same two E1 fixtures through the Round-37-scope variant:
`E1 payload=…,round36-final-lane-commits=1,bound=0 closed=0` (unbound) and `E1 payload=placeholders=1,… closed=0`
(placeholder) while the green control stays `closed=9/9 exit=0`. So the fixture is not tied to the round-36
heading: swapping `## Round 36` → `## Round 37` in the fixture is the whole difference.

**E14 against the real predecessor bytes.** `standin.sh E14` on a tree whose
`corpus/instruments/r37-closure.sh` is a byte copy of the committed `r36-closure.sh`:
`E14 payload=suite-present=1,porcelain-default=1,status-swallow=1 closed=0`. The shape check therefore rejects
the instrument the round-37 suite replaces — it is not a check the r36 code already satisfies.

## 3. E9 limb (b) measured open on the inherited suite — D6 is real, and the fixture proves it

Corrupt-index fixture (`printf 'CORRUPT-INDEX' > .git/index` after a clean commit):

```
$ ( cd fx/e9-corrupt.* && git status --porcelain ); echo rc=$?
fatal: .git/index: index file smaller than expected
rc=128
$ ( cd fx/e9-corrupt.* && git status --porcelain 2>/dev/null | grep -c . )
0
```

The inherited suite on that same fixture, its own line:

```
E9 payload=status-dirty=0,scratch-seat-dirs=0,head-match=1,lane-root=1,scratch-root=present closed=1
closed=8/9 exit=1     # the red here is E4 tracked-index=0 (ls-files also fails on the corrupt index)
```

i.e. **E9 reads clean while the status read exits 128** — the D6 fail-open limb, observed, not argued. The
fail-closed stand-in on the same repo returns `E9 payload=status-read=failed,… closed=0`, and on the clean
fixture repo `status-read=ok,…,closed=1` (so the limb is not red-by-construction).

## 4. Fixture-shaping findings the suite builder needs (each one cost me a run)

1. **E1's 4-line window is wider than it looks.** The r36 E1 collects 40-hex tokens on a `[Ff]inal lane commit`
   line **or the four lines after it**. Two consequences measured on my first green fixture (which read
   `round36-final-lane-commits=2,bound=1`, `closed=0`):
   - the `Anchor ancestor (round-36 lane head): c20300df…` line sat 4 lines below the historical
     `Final lane commit:` line and was swept into the binding set, where it can only be unbound;
   - a prose comment containing the words “final lane commit” opens a window of its own.
   The green fixture therefore keeps ≥5 lines between any `Final lane commit:` line and the next 40-hex token.
   The r37 suite inherits this: if the real round-37 SCORECARD puts the anchor-ancestor hash within four lines
   of a `Final lane commit:` line, E1 will read unbound for a reason that has nothing to do with the closure.
2. **E13 must split on unescaped pipes.** My first stand-in used `awk -F'|'`; the markdown cell `gate\|probe`
   then yields field 3 = `gate\`, which strips to `gate` and **accepts the exact D5 defect**. The stand-in now
   protects `\|` (→ `\001`) before splitting. Any counter that parses registry rows by raw `|` will read
   `gate\|probe` as the single choice `gate`; the fixture `e13-typepipe` is the probe for that.
3. **`local t=$1 f=$t/…` is unbound under `set -u`** (all words expand before `local` takes effect). Any
   harness written to `set -uo pipefail` must split that into two statements; my stand-in's first run died on
   it on all five checks before the fix.
4. **The r36 suite's E9 `scratch-root` payload is `present|absent`.** A missing `--scratch-root` reads zero seat
   dirs and looks green; the fixtures always pass an existing empty directory so `scratch-root=present` is in
   the payload.

## 5. Wiring for the r37 suite's `--selftest` (so `cases=14 failures=0` means something)

The r36 precedent is `selftest_case_E<n>` with `st_pos` (positive on the export) + `st_neg <ID> <label> <tree>
<ref> <needle>` fixtures built by `mut_put` under `$MUT`. These fixtures transplant directly: one
`mut_reset "$MUT/E<n>-…"; printf … | mut_put …` block per row of §2, and the needle is the payload substring in
the “expected needle” column — each names the reopened limb (`bound=0`, `placeholders=1`, `erratum-row=0`,
`registry-r36-closure=0`, `provenance-note=0`, `claims-erratum-d5=0`, `correction-round35=0`,
`supersedes-r23=0`, `stale-line=1`, `names-corrected-line=0`, `status-dirty=1`, `digest-match=0`,
`payload-lines=13`, `names-false-path=0`, `named-correction=0`, `stale-e666d902-label=1`,
`anchor-ancestor-label=0`, `type-single=0`, `verdict-exit2-could-not-evaluate=0`, `porcelain-default=1`,
`status-swallow=1`, `status-read=failed`). Every fixture above is a single-clause edit of one green base, so a
`st_verdict` that requires **all** mutants of a check rejected cannot be satisfied by a fixture that merely
breaks the whole tree.

## 6. Limits (measured, not hidden)

- The r37 instrument is absent at this read; E1–E9 rejection is shown on the **inherited** suite's code (the
  frozen claim keeps those nine checks verbatim), E1 additionally on a Round-37-scope variant of that code, and
  E10–E14 on a stand-in written to the claim. The r37 suite must (a) carry `Round[- ]?37` in E1's scope, and
  (b) re-run these fixtures against **its own** bytes; this receipt does not assert that code.
- The stand-in's E10 digest limb compares against `corpus/instruments/r37-closure.sh` in the export, per the
  claim; the r37 suite should self-digest `BASH_SOURCE` the way the r36 suite prints `suite-sha256=`, and the
  fixture header must carry **that** digest.
- E12's lesson limb (`lesson-anchor-ancestor`) has no dedicated mutant here; it is green in every fixture and
  red would be produced by dropping the label from `corpus/lessons/round-37.md`. The SCORECARD limbs are
  covered by `e12-stale` and `e12-nolabel`.
- Nothing here is a claim of closure: it is the discriminating set the round-37 `--selftest` needs, with each
  rejection observed once.

## 7. Write scope

Lane writes: this receipt only. Scratch tree `/fast/scratch/hyaku/kasegi-r37/ExecC1Fixtures`
(`build.sh` sha `68a480f79fc7ae2e1fe39f280ee34d83c6ada6afa7ad288fdfab0afb9d8811ce`, `standin.sh` sha
`2d5c9191cae6f4e252a21efb5811bdaf30fcb51a697171a17fce416be0de21fe`, `r37-e1-variant.sh` sha
`d4b2c618cbe0a1a756468513f4fb09d8dd34b1f2f1ab8a21af62c3d08ed1ae05`) removed before yield. No lane, fleet,
sibling-lane or source-tree file was modified; no git mutation ran outside the verified fixture repos.

Report: `.ufo/waves/round-37/wave1/ExecC1Fixtures.md`
