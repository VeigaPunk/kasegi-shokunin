# ScribeMistakes — round-37 Mistakes rows (M37-1…M37-5)

seat `ScribeMistakes` · role scribe · milestone round-37 · axis depth:verifiability
lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (the only repo read or written)
dispatch: inline spawn handoff, hyaku run 9 (L1 `KasegiR37`)

Revisions read (read-only): lane `HEAD` `b362068195d5489aa94b31e6ec8f880c367e0ba0`; round-37 base
`b56a41680cefd391868c1c370dc063c69d827e7d`; claims-freeze `224df74db2a46d627ae1475a72ca48796bbd177c`;
r36 base `cc692008b0cfd58d18275aa6c4aed79620120799`; r36 judged head
`a23dc4788aa7c98831eed6db953434034ce5ae8d`; r36 lane head
`c20300df516eb5575d8db2aaad1f0cf4913e7981`.

Method: plain reads over committed bytes (`git show`/`cat-file`/`ls-tree`/`merge-base`, `grep`,
`sed`, `awk`, `sha256sum`) plus the two wave receipts named per row. **No gate or instrument was
executed** — the r37 suite is not in any tree at this head (`cat-file -e HEAD:corpus/instruments/r37-closure.sh`
→ 128), so every "green" below is the frozen claim's declared after-state, not a run I observed.

## 1. What this seat produced

The paste-ready `## Mistakes` table for `corpus/lessons/round-37.md` (§2), with each row's derivation
measured at the revisions above (§3), its `captured-by` criterion named (§4), and its fix bound to the
frozen C1 checks E10–E14 (§5). No lane file other than this receipt was written; the lesson itself is
another seat's artifact and consumes this table verbatim.

## 2. Deliverable — paste-ready `## Mistakes` table

| id | class | event | evidence | captured-by | fix | able to fail |
|---|---|---|---|---|---|---|
| M37-1 | evidence-record | Round-36 C1 committed only the negative limbs. `.ufo/waves/round-36/final-gates/all-gates.txt` at the judged head carries the three forged-selftest rejections and the two reds (`closed=0/9 exit=1`, `closed=3/9 exit=1`); it carries no `suite-sha256=` header, no `E<n> payload=` line, no `closed=9/9`, no `selftest case=` line, no `cases=` summary. The positive run existed only as prose in the SCORECARD "measured closure" line and the report erratum. The wave's receipts were swept mid-flight — two seats' scratch dirs were removed before the final gate run — and no positive transcript from any run reached the committed gates file. | `corpus/lessons/round-36-verifier-spotcheck.md` §2 C1 evidence gap / §5 D1. Measured: 28-line `all-gates.txt` at `a23dc478`; 0 matches for each of the five E10 token classes (`suite-sha256=`, `E[0-9]+ payload=`, `closed=9/9`, `^selftest case=`, `^cases=[0-9]+ failures=[0-9]+`); file absent at `cc692008` (`git cat-file -e` exit 128). Incident: `.ufo/reports/round-36/kasegi.md:12` ("two seats' scratch dirs were swept before the final gate run"), `.ufo/waves/round-36/wave1/MutC2Entry.md:98-99`. | none (new) — R28 binds the run to an export of a named head and a quiescent lane, not to the run's own transcript | E10: the export's `.ufo/waves/round-37/final-gates/all-gates.txt` carries `suite-sha256=<sha>` (sha = digest of the suite bytes), fourteen `E<n> payload=` lines, `closed=14/14 exit=0`, fourteen `selftest case=` lines and `cases=14 failures=0` | r36 base export: file absent (cat-file 128) → red; r36 judged-head export: file present but 0 of the five token classes → red; final head with the head-named transcript → green |
| M37-2 | fail-open-gate | r36 E9 read the lane's status as `git --no-optional-locks -C "$srepo" status --porcelain 2>/dev/null` piped to `count_lines`, then assigned `porcelain=${porcelain:-0}` (`r36-closure.sh:465-466`): a status read that failed was scored 0 dirty lines, i.e. clean. The same limb's runtime face: two concurrent quiescence sweeps wiped `/fast/scratch/hyaku/kasegi-r36/*` mid-wave — one destroyed a mutation seat's probe mid-run — and the L1 swept two seat dirs before the final gate run, so the limb's clean reading could be produced by deleting the evidence it reads. | Suite `sha256 4db1ae70c76afd28b29e9ec24c2e44835322c61fa33e30c966f75ce0dfadb7c4` (894 lines) at `c20300df`: `grep -cF 'porcelain:-0'` → 1 (line 466); `2>/dev/null` on the status read at line 465; 41 `2>/dev/null` in the file. Incident: `MutC2Entry.md:98-99`, `ExecQuiescenceProbe.md:116-117` (seat-dir counter 46→41→36→35 across the wave), `.ufo/reports/round-36/kasegi.md:12`. | none (new) — R28 required quiescence but no criterion required the limb to fail closed on a failed read | E14: the suite's quiescence code is fail-closed by shape (`grep -cF 'porcelain:-0' r37-closure.sh` → 0; no status-read `2>/dev/null` swallow) + QUALITY R30 (round-37 append, fail-closed gate) | the r36 suite bytes are the standing mutant (1 `porcelain:-0`): a reintroduced `${porcelain:-0}` / `2>/dev/null` status read → E14 red; landed suite → 0 |
| M37-3 | stale-premise / label-drift | Round-36 lesson line 3 and `SCORECARD.md:1492` (inside `## Round 36`) name `e666d902337a49dcbfc77880939874f39c6f477b` as the round's "final lane commit" — an intermediate ancestor. The round's own measured-closure line records `274fa9ae`, the judged head is `a23dc478`, and the round-36 lane head (branch tip) is `c20300df`. | Measured: `corpus/lessons/round-36.md:3` at `a23dc478` and at `HEAD`; `grep -cF 'Final lane commit: e666d902' SCORECARD.md` → 1 (line 1492); ancestry `anc=0` for `a23dc478→c20300df→b56a416`; `corpus/lessons/round-36-verifier-spotcheck.md` §5 D4 ("Label it as the anchor ancestor", :156). | R2 (self-description is a claim) / R19 (a literal a record quotes must be produced by a command the record cites) | E12: the round-37 lesson and the round-37 SCORECARD section label r36 lane head `c20300df` as `anchor ancestor`; the stale label `Final lane commit: e666d902` appears nowhere inside the round-37 SCORECARD section | a round-37 section carrying the copy-forwarded `Final lane commit: e666d902…` (the literal exists once at `:1492`, so copy-forward is the realistic mutant) → E12 red; the landed section naming `c20300df` as `anchor ancestor` → green |
| M37-4 | counter-discrimination | `SKILL.md:1111` registers `r36-closure.sh` with a type cell whose value is the two-valued literal `gate\|probe` (raw bytes: backslash-escaped pipe) instead of one of the registry's single choices, and its verdict map stops at `exit 0 only for K=9`: the suite's plain-run refusal `exit 2` — its export-mode guard — has no verdict, so `could-not-evaluate` is unrepresented in the row. The r36 row's entry command itself documents "a plain run refuses with exit 2". | Measured at `c20300df` and `HEAD b3620681`: row `:1111`; `grep -cF 'gate\|probe' SKILL.md` → 6 rows (five besides the r36 row: `limb-mutation-check.py`, `capture-binding-check.py`, `r-defect-closure.sh`, `kill-rule-check.py`, `r35-defect-closure.sh`); the verdict cell ends "exit 0 only for K=9" with no exit-2 arm; `corpus/lessons/round-36-verifier-spotcheck.md` §5 D5. | R29 (an instrument is registered under its exact basename; the registry row is where its verdict shape is published) | E13: the `r36-closure.sh` row has a single-choice type cell (not the literal `gate\|probe`) and its verdict map includes exit `2` → `could-not-evaluate` | a fixture row with the type cell `gate\|probe` and no exit-2 verdict (today's bytes, measured) → red; single-choice type + exit-2 verdict → green |
| M37-5 | stale-premise | `LOG.md:1665` (the round-36 C1 bullet) states that the round landed `corpus/instruments/r36-closure.sh` + `corpus/instruments/r36-fixtures/`. The fixtures directory is in no r36 tree, and LOG is append-only, so the false statement stands as filed. | Measured: `:1665` under `## Round 36` (`:1661`) names `corpus/instruments/r36-fixtures/`; `git ls-tree -r --name-only <rev> \| grep -c r36-fixtures` → 0 at `c20300df`, `a23dc478` and `HEAD`; `corpus/lessons/round-36-verifier-spotcheck.md` §5 D2. | R9 (append the correction to a historical log rather than silently rewriting the filed assertion) | E11: the `LOG.md` round-37 entry contains a named correction of the round-36 C1 bullet's false `corpus/instruments/r36-fixtures/` path | a tree whose LOG has no round-37 correction → red (measured: `grep -c '^## Round 37' LOG.md` → 0 at `HEAD`); a round-37 entry that names the correction → green |

## 3. Derivation — commands and observed output

Every command below ran read-only from the lane root against committed bytes; `git` was invoked as
`/usr/bin/git` (one inherited temp shell resolved `git` to nothing — `/home/vgpnk/.local/bin/git` does
not exist — so the absolute path pins the binary).

### M37-1 — the positive limb never reached the committed gates file

```
$ /usr/bin/git show a23dc478:.ufo/waves/round-36/final-gates/all-gates.txt | wc -l
28
$ /usr/bin/git show a23dc478:.ufo/waves/round-36/final-gates/all-gates.txt \
    | grep -cE 'suite-sha256=|E[0-9]+ payload=|closed=9/9|^selftest case='
0
$ /usr/bin/git show a23dc478:.ufo/waves/round-36/final-gates/all-gates.txt \
    | grep -cE '^cases=[0-9]+ failures=[0-9]+'
0
$ /usr/bin/git cat-file -e cc692008:.ufo/waves/round-36/final-gates/all-gates.txt; echo $?
fatal: path '.ufo/waves/round-36/final-gates/all-gates.txt' exists on disk, but not in 'cc692008'
128
```

The 28 committed lines are exactly: `== selftest ==` + three `selftest judge=forged-* rejected=1`
lines, `== neg base == closed=0/9 exit=1`, `== neg judged == closed=3/9 exit=1`, and the C2 block.
There is no `suite-sha256=` header, no `E<n> payload=` line, no `closed=9/9`, no `selftest case=`
line and no `cases=… failures=…` summary — none of the five token classes E10 requires. The three
`judge=forged-*` lines prove the selftest *judge* rejects forgeries; they do not carry the selftest
*verdicts* of the head.

Incident context (quoted, not inferred): `.ufo/reports/round-36/kasegi.md:12` — "receipt count 60/64
and two seats' scratch dirs were swept before the final gate run"; the report's erratum (:87) records
the clean re-run at `c20300df` as prose. `MutC2Entry.md:98-99` records the root being wiped twice by a
concurrent quiescence sweep at 12:57 and between two tool calls. These are the conditions under which a
single stable transcript was not preserved; the row records the missing receipt, not a causal proof.

### M37-2 — the failed status read was mapped to clean

```
$ /usr/bin/git show c20300df:corpus/instruments/r36-closure.sh | sha256sum
4db1ae70c76afd28b29e9ec24c2e44835322c61fa33e30c966f75ce0dfadb7c4  -
$ /usr/bin/git show c20300df:corpus/instruments/r36-closure.sh | wc -l
894
$ /usr/bin/git show c20300df:corpus/instruments/r36-closure.sh | grep -cF 'porcelain:-0'
1
$ /usr/bin/git show c20300df:corpus/instruments/r36-closure.sh | grep -cF '2>/dev/null'
41
$ /usr/bin/git show c20300df:corpus/instruments/r36-closure.sh | sed -n '465,466p'
  porcelain=$(git --no-optional-locks -C "$srepo" status --porcelain 2>/dev/null | count_lines)
  porcelain=${porcelain:-0}
```

The digest equals the one the round-36 verifier spot-check re-derived at `a23dc478` (`4db1ae70…`,
§2 C1), so the mutant I measured is the byte-identical suite bytes that round judged — not a worktree
variant. The failing read (`2>/dev/null`) produces an empty `count_lines` pipeline, and `${porcelain:-0}`
turns that into the clean answer. E9 therefore could not distinguish "nothing dirty" from "could not
read".

Runtime face, quoted: `ExecQuiescenceProbe.md:116-117` — "seat scratch dirs exist until the sweep …
The seat-dir counter moved 46 → 41 → 36 → 35"; `MutC2Entry.md:98-99` — "`/fast/scratch/hyaku/kasegi-r36/*`
was wiped by a concurrent quiescence sweep at 12:57 (destroying this seat's first probe mid-run) and
again between two tool calls". The limb's subject (scratch state) was being mutated by the enforcement
itself, which is why a fail-closed read, not a swept-clean read, is the fix.

### M37-3 — `e666d902` named as final

```
$ sed -n '3p' corpus/lessons/round-36.md | grep -o 'final lane commit `[0-9a-f]*`'
final lane commit `e666d902337a49dcbfc77880939874f39c6f477b`
$ /usr/bin/git show a23dc478:SCORECARD.md | grep -nF 'Final lane commit: e666d902'
1492:Final lane commit: e666d902337a49dcbfc77880939874f39c6f477b
$ /usr/bin/git show a23dc478:SCORECARD.md | grep -n '^## Round 36'
1406:## Round 36 — frozen claims C1/C2 (2026-10-26)
$ /usr/bin/git merge-base --is-ancestor a23dc478 c20300df; echo $?
0
$ /usr/bin/git merge-base --is-ancestor c20300df b56a416; echo $?
0
```

`c20300df` is a descendant of the judged head `a23dc478` and an ancestor of the round-37 base
`b56a416`; the label at `:1492` names a commit four positions behind the round-36 tip. The spot-check
already routed the correction and named the replacement (`…-spotcheck.md:156`: "Label it as the anchor
ancestor"). The string exists exactly once in SCORECARD, so a copy-forward into the round-37 section is
the realistic mutant E12 must kill.

### M37-4 — the registry type cell and the missing exit-2 verdict

```
$ grep -n '^| r36-closure.sh' SKILL.md | cut -c1-200
1111:| r36-closure.sh | gate\|probe | `bash corpus/instruments/r36-closure.sh --export-ref <hash>` (export-mode only; a plain run refuses with exit 2) | one `E<n> payload=… closed=0\|1` line per che
$ sed -n '1111p' SKILL.md | grep -c 'could-not-evaluate'
0
$ sed -n '1111p' SKILL.md | grep -c 'exit 2'
1
$ grep -cF 'gate\|probe' SKILL.md
6
$ /usr/bin/git show c20300df:SKILL.md | grep -cF 'gate\|probe'
6
```

The second cell's raw bytes are `gate\|probe` — a backslash-escaped pipe, so the rendered cell value is
the literal `gate|probe`, a two-valued string where the same registry column elsewhere holds a single
choice (`reporter (read-only, NOT a claim)`, one row at this head). Five other rows carry the
`gate\|probe` form; E13 is scoped to the `r36-closure.sh` row, per the frozen C1 predicate. The row
mentions `exit 2` exactly once — in its **entry command** cell ("a plain run refuses with exit 2") —
and its **verdict map** cell contains no exit-2 arm and no `could-not-evaluate` token (`grep -c` on the
row → 0/1 as above). A reader of the verdict map alone therefore cannot tell a refusal from a pass.

### M37-5 — the false path in the append-only log

```
$ sed -n '1661p' LOG.md | cut -c1-150
## Round 36 — 2026-10-26 — C1 head-closure suite E1–E9 over `git archive` exports + C2 F19 FIRST EPSS admitted (one v2 wave, 64 seats)
$ sed -n '1665p' LOG.md | cut -c1-150
- **C1 depth:verifiability (4 held) — head-closure suite over exports.** Landed `corpus/instruments/r36-closure.sh` + `corpus/instruments/r36-fixtur
$ /usr/bin/git ls-tree -r --name-only c20300df | grep -c r36-fixtures
0
$ /usr/bin/git ls-tree -r --name-only a23dc478 | grep -c r36-fixtures
0
$ /usr/bin/git ls-tree -r --name-only HEAD | grep -c r36-fixtures
0
```

The fixtures directory is asserted as landed and is absent from all three trees. LOG is append-only
(the round-36 entry itself opens with a claims-freeze line and no rewrites), so the correction is an
appended round-37 entry that names the false path — the E11 shape — not an edit of `:1665`.

## 4. `captured-by` rationale

- **M37-3 → R2 / R19.** R2: "Self-description is a claim: a rate cites its census file, a `$VARIABLE`
  cites the code that reads it, a deletion count cites the command" (`corpus/QUALITY.md`, round-22
  block) — a "final lane commit" label is the lane describing its own landing. R19: "A specimen figure
  quoted inside a record row is either produced by a command the row cites or backed by a closure
  check that reproduces it" — a commit named as final must be the commit the final measurement ran at.
- **M37-4 → R29.** R29 places an instrument's registration at the `SKILL.md` § Gates & probes registry
  and makes the row's shape load-bearing ("An instrument is registered … under its exact basename —
  one row whose name cell is exactly the file name"). The type cell and verdict map are that row.
- **M37-5 → R9.** R9: "A numerical erratum names its base and changed-file scope … Append the
  correction to historical lessons/logs rather than silently rewriting their filed assertions."
- **M37-1 / M37-2 → none (new).** R28 requires a run over `git archive <final lane commit>` on a
  quiescent lane; it says nothing about committing the run's own transcript (M37-1), and nothing about
  the limb's failure direction (M37-2). Neither class had a criterion before this round.

## 5. Fix binding to the frozen C1 checks

From `.ufo/waves/round-37/claims.json` C1 `predicate` (frozen at
`224df74db2a46d627ae1475a72ca48796bbd177c`, before any seat scored): E10 = D1, E11 = D2, E12 = D4,
E13 = D5, E14 = D6; E1–E9 carry the round-36 semantics. The required-reds limb is "r36 base export →
`closed<14/14 exit=1`; r36 judged-head export → `closed<14/14 exit=1` (E10–E14 open there)". My
read-only proxies for that limb, above, are E10's five token classes (0 each at `a23dc478`, file absent
at `cc692008`), E11's correction absent at `HEAD` (`## Round 37` count 0), E12's round-37 lesson absent
(`cat-file -e HEAD:corpus/lessons/round-37.md` → 128), E13's defect still open at `HEAD` (six
`gate\|probe` rows, r36 row `:1111`), and E14's target suite absent (`cat-file -e
HEAD:corpus/instruments/r37-closure.sh` → 128). None of these is a suite run; the suite's own reds are
the executor seats' evidence, not this seat's.

QUALITY R30 is **not present** in `corpus/QUALITY.md` at `b3620681` (the file's last row is R29; no
`R30` token exists). M37-2's fix cites it as the round-37 append this wave lands — the lesson must not
cite R30 as landed until the QUALITY append commit exists.

## 6. Limits (what this seat did not observe)

- The r37 suite (`corpus/instruments/r37-closure.sh`), its fixtures, `.ufo/waves/round-37/final-gates/all-gates.txt`,
  the round-37 lesson and the round-37 SCORECARD section did not exist in `HEAD` (`b3620681`) or in the
  round-37 base `b56a416` at write time (`cat-file -e` → 128 for each of the three paths; `## Round 37`
  heading count 0 in `LOG.md` and `SCORECARD.md` at `b56a416`). Every "green" in §2 is the frozen
  claim's after-state; the greens are owed by the integration commit and verified by the seats that run
  the suite.
- E13's "single-choice type cell" is quoted from the frozen predicate; the exact allowed choice
  (`gate` vs `probe`) is the suite's definition, not something I re-derived.
- E10's `suite-sha256=<sha>` binding (sha == digest of the suite bytes) was not exercised: the suite
  bytes are absent, so there is no digest to compare.
- The r36 scratch-sweep incident is reported as its receipts state it (`MutC2Entry.md`,
  `ExecQuiescenceProbe.md`, report `:12`); I did not re-run any seat or inspect the sweeper.

## 7. Writes, scratch, tooling

- Lane writes: this receipt only. No lane file edited, no commit, no mutating git command.
  `git status --porcelain` was read twice (start and end of the seat; both times only the untracked
  round-37 wave entries), and the ancestry checks used `merge-base --is-ancestor` (read-only).
- Scratch: `/fast/scratch/hyaku/kasegi-r37/ScribeMistakes/` (bound explicitly, not via `TMPDIR`)
  held one `facts.txt` transcript; the receipt was written and corrected first, then the scratch dir was
  removed before yield. `/tmp` unused.
- Tooling: none installed, none upgraded; no pacman transaction. Only `/usr/bin/git`, coreutils,
  `grep`/`sed`/`awk`/`sha256sum` were used.
