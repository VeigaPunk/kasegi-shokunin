# ExecC1SuiteBuild — `r36-closure.sh` DRAFT (C1, depth:verifiability)

Seat: `ExecC1SuiteBuild` (leaf executor, round 36). Item: write the committed instrument
`corpus/instruments/r36-closure.sh` as a DRAFT for the L1 to land. **I wrote no lane file but this
receipt. The L1 landed this draft at `corpus/instruments/r36-closure.sh` in integration commit
`caa3146` ("round-36: integration — r36-closure suite, …"), byte-identical to the frozen digest
below (`sha256sum` of the landed file = `4db1ae70…`, 39 022 bytes). Integration and every later
commit are the L1's; I did not touch the landed file.**

## Frozen draft identity

| field | value |
|---|---|
| draft path (scratch) | `/fast/scratch/hyaku/kasegi-r36/ExecC1SuiteBuild/r36-closure.sh` |
| intended lane path (L1 lands) | `corpus/instruments/r36-closure.sh` — **landed at `caa3146`, digest equal** |
| sha256 | `4db1ae70c76afd28b29e9ec24c2e44835322c61fa33e30c966f75ce0dfadb7c4` |
| lines / bytes | 894 / 39 022 |
| `bash -n r36-closure.sh` | exit 0 (`SYNTAX_OK`), at the frozen digest |
| tools installed | none (no pacman/uv/npx/official-binary install was needed) |
| lane writes | this receipt only; scratch dir removed at yield |

The digest moved six times under review (`1019d64d` 710 → `9fbdee69` 780 → `dc5208fa` 774 →
`76273416` 817 → **`4db1ae70` 894**). Every move repaired a measured survivor, a measured lane
write, or a measured report-binding gap, and each was announced to the seats that had pinned the
previous digest. The verbatim text is at the end of this receipt so the bytes survive scratch
cleanup.

## ⚠ Blocking hand-off for the L1 (read this first)

The final `closed=9/9` needs **four** artifacts that do not exist at `b47f2cd`, plus a clean tree:

1. **A round-36 SCORECARD section carrying a bound `Final lane commit:` line.** E1 scans the LAST
   `#{1,4} …Round[- ]?36…` heading block in `SCORECARD.md` and requires >= 1 40-hex on a
   `[Ff]inal lane commit` line (or the four lines after it) that exists in the lane repo and is an
   ancestor of the exported ref. History alone no longer satisfies E1 (that was a measured
   survivor). House form: a `## Round 36 …` heading, then `**Final lane commit: `<hash>`**`.
   A self-reference is accepted (`merge-base --is-ancestor X X` exits 0, verified).
2. **Two SKILL.md registry rows** inside a `## …Gates & probes registry…` section, first cell the
   exact basename: `| r35-defect-closure.sh | gate\|probe | … |` and `| r36-closure.sh | … |`.
   Prose, `.bak`/`.old` rows, or rows under another heading do not close E3.
3. **`.ufo/waves/round-35/wave1-results.json.provenance.md`**, committed, non-empty (mirror
   `.ufo/waves/round-34/wave1-results.json.provenance.md`, 5639 bytes).
4. **`corpus/lessons/round-36.md`** carrying the `M36` rows AND naming `source-recheck` (the
   instrument whose output was the false evidence line). Do **not** quote
   `source-recheck exit 0 on committed bytes` into `corpus/lessons/round-35.md` — E8's absence limb
   is file-wide on that lesson because the frozen counter is; at HEAD it already reads 0, so leave
   it alone and put the correction in the round-36 lesson.
5. **Quiescence at filing:** commit every round-36 dispatch file and receipt (`git status
   --porcelain` empty), remove all `/fast/scratch/hyaku/kasegi-r36/*` seat dirs, run with
   `--export-ref <the lane HEAD at run time>`, and keep `--work` outside the scanned scratch root.
   Also commit `corpus/instruments/r36-closure.sh` itself.

Nothing else is outstanding: E2, E5, E7, E6 are already green at HEAD, and the negative controls are
green as negatives.

## Interface (as implemented)

```
bash corpus/instruments/r36-closure.sh --export-ref <hash> [--lane DIR] [--work DIR]
                                       [--scratch-root DIR]
bash corpus/instruments/r36-closure.sh --selftest [--export-ref <hash>] [--lane DIR]
                                       [--work DIR] [--scratch-root DIR]
bash corpus/instruments/r36-closure.sh -h|--help
bash corpus/instruments/r36-closure.sh            # refused, exit 2
```

- **Export mode only.** `--export-ref <hash>` resolves the ref with `git -C <lane> rev-parse
  --verify <hash>^{commit}`, then `git -C <lane> archive --format=tar <hash> | tar -xf - -C
  <work>/export`; every check reads its bytes under that export root with relative paths after a
  `cd`. There is **no** `--root DIR` mode and no live-tree run: a plain invocation prints
  `refusing to run against the live worktree: this suite is export-mode only.` and exits 2.
- **Lane path normalisation.** `--lane` is resolved to an absolute physical path at entry, so a
  relative `--lane` works from any cwd (it used to resolve against the export tree inside E1's
  subshell and read a false red).
- **Temp/work.** `--work DIR` if given, else `mktemp -d -t r36-closure.XXXXXXXX` (TMPDIR honoured by
  mktemp; the script contains **no** `/tmp` literal). `<work>/export` and `<work>/mut` are cleared
  before extraction (a pre-seeded export cannot satisfy a check), and `--work` is refused with exit
  2, **before `mkdir`**, when it resolves inside the lane.
- **Report binding.** The run header is
  `export-ref=<sha> mode=export lane=<abs> suite-sha256=<sha of the executing file>`, and the
  selftest header is the same with `selftest` in place of `mode=export`. A non-default `--lane` or
  `--scratch-root` additionally prints a non-gating `deviation=non-default --…` line, so an
  operator override is visible rather than silent.
- **Output.** One `E<n> payload=<comma-list> closed=0|1` line per check, then `closed=K/9 exit=0|1`.
  Exit 0 only for K=9; exit 1 while any check is open; exit 2 on harness error. The summary is
  re-derived from the printed payload lines (`suite problem=self-report` when fewer than nine or the
  count disagrees), so a partial run cannot print a green summary.
- **Git surface:** read-only `archive`, `rev-parse`, `cat-file -e`, `merge-base --is-ancestor`,
  `ls-tree -r --name-only`, `ls-files`, and `status --porcelain` **with `--no-optional-locks`** so
  the status read does not take `.git/index.lock`. `git init/add/commit` occur only inside a `--work`
  fixture whose `rev-parse --show-toplevel` is verified equal to the fixture dir.
- **Selftest:** positive limb = every check passes on the export (default `HEAD`); mutant limb = one
  to five scratch fixtures per check, each reopening exactly one clause, whose rejection must name
  that clause. `judge_selftest_report` accepts a report only when it carries nine distinct
  `selftest case=E<i> … verdict=pass` lines, one `selftest cases=9 failures=0`, **and** for each id
  exactly `n` `selftest detail=E<i> mutant=` lines of which `ok` say `rejected=1`, matching that
  case's `mutants=ok/n` with `n >= 1` — so a fabricated case line claiming `mutants=0/0` is rejected.
  Four forged reports are rejected and printed as evidence.

## The nine checks, limb by limb

| id | rejects when | limbs (payload names) |
|---|---|---|
| E1 | placeholder, unresolvable/branch-local closure hash, or a closure section with no bound line | `placeholders` (`filled by the L1`) and `lane-hash-markers` (`<LANE_HASH>`) == 0; `round36-section` == 1; every 40-hex on a `[Ff]inal lane commit` line in the last `Round[- ]36` block (+4 lines) must satisfy `cat-file -e <h>^{commit}` and `merge-base --is-ancestor <h> <export-ref>`; `round36-final-lane-commits >= 1`, `bound == total` |
| E2 | round-34 depth:density erratum missing or only quoted in prose | `erratum-marker` (`Erratum (round 35)`) >= 1 **and** `erratum-row` (`^\| depth:density \| 9 \| mean \*\*201\.2\*\*`) >= 1 **and** `erratum-mean` (`201\.2`) >= 1 |
| E3 | registry rows absent, inexact, mentioned, or outside the registry section | `registry-r35-defect-closure`, `registry-r36-closure`: table rows inside a `## …Gates & probes registry…` section (closed by the next `## ` heading), first cell the exact basename (optional backticks) |
| E4 | round-35 results untracked or provenance note absent/empty | `tracked-ref` (`ls-tree -r --name-only <ref> -- .ufo/waves/round-35/wave1-results.json` == 1), `tracked-index` (frozen `git ls-files` == 1), `provenance-note` (`<path>.provenance.md` present and non-empty) |
| E5 | claims erratum absent or empty | `claims-erratum-d5` = `.ufo/waves/round-35/claims-erratum-d5.md` exists as a **non-empty regular file** |
| E6 | round-34 integration receipt lacks the correction | path derived from the export's own `ls-tree` (exactly one `…/.ufo/waves/round-34/wave1/L1Integration.md`, `corpus/instruments/` copies excluded; 0 or 2 candidates fail closed); `correction-round35 >= 1` |
| E7 | supersession rows absent or only quoted in prose | `supersedes-r22`, `supersedes-r23`: QUALITY.md table rows whose third column begins `supersedes R22`/`R23` |
| E8 | correction missing, unnamed, or stale line retained | `m36-rows` (`M36` in `corpus/lessons/round-36.md`) >= 1; `names-corrected-line` (`source-recheck` there) >= 1; `stale-line` (the false-evidence string in `corpus/lessons/round-35.md`) == 0; `round35-lesson` == 1 |
| E9 | lane not quiescent, or a status repo that is not the lane root | `lane-root` (status repo's `--show-toplevel` equals its physical path); `status-dirty` (`git --no-optional-locks status --porcelain` line count) == 0; `scratch-seat-dirs` (immediate child **dirs** of the scratch root, the suite's own `--work` excluded) == 0; `head-match` (`rev-parse HEAD` == resolved export ref); `scratch-root=present\|absent` reported for visibility (non-gating) |

## Measured evidence at the frozen digest

### Export runs (exact stdout)

```
$ bash r36-closure.sh --export-ref 3266c9937b03062d9bbc2f436e20820115ed179c --scratch-root <empty>
export-ref=3266c9937b03062d9bbc2f436e20820115ed179c mode=export lane=/home/vgpnk/Projects/shokunin/kasegi-shokunin suite-sha256=4db1ae70c76afd28b29e9ec24c2e44835322c61fa33e30c966f75ce0dfadb7c4
deviation=non-default --scratch-root
E1 payload=placeholders=1,lane-hash-markers=0,round36-section=0,round36-final-lane-commits=0,bound=0 closed=0
E2 payload=erratum-marker=0,erratum-row=0,erratum-mean=0 closed=0
E3 payload=registry-r35-defect-closure=0,registry-r36-closure=0 closed=0
E4 payload=tracked-ref=0,tracked-index=1,provenance-note=0 closed=0
E5 payload=claims-erratum-d5=0 closed=0
E6 payload=path=.ufo/waves/round-34/wave1/L1Integration.md,correction-round35=0 closed=0
E7 payload=supersedes-r22=0,supersedes-r23=0 closed=0
E8 payload=m36-rows=0,names-corrected-line=0,stale-line=0,round35-lesson=0 closed=0
E9 payload=status-dirty=9,scratch-seat-dirs=0,head-match=0,lane-root=1,scratch-root=present closed=0
closed=0/9 exit=1
```
exit 1 — **0/9 on the r35 base export**, as the frozen claim requires.

```
$ bash r36-closure.sh --export-ref 0aee0ef105395a2f1d6ace7eaeef13871bb26988 --scratch-root <empty>
export-ref=0aee0ef105395a2f1d6ace7eaeef13871bb26988 mode=export lane=/home/vgpnk/Projects/shokunin/kasegi-shokunin suite-sha256=4db1ae70c76afd28b29e9ec24c2e44835322c61fa33e30c966f75ce0dfadb7c4
deviation=non-default --scratch-root
E1 payload=placeholders=1,lane-hash-markers=0,round36-section=0,round36-final-lane-commits=0,bound=0 closed=0
E2 payload=erratum-marker=1,erratum-row=0,erratum-mean=3 closed=0
E3 payload=registry-r35-defect-closure=0,registry-r36-closure=0 closed=0
E4 payload=tracked-ref=0,tracked-index=1,provenance-note=0 closed=0
E5 payload=claims-erratum-d5=1 closed=1
E6 payload=path=.ufo/waves/round-34/wave1/L1Integration.md,correction-round35=1 closed=1
E7 payload=supersedes-r22=1,supersedes-r23=1 closed=1
E8 payload=m36-rows=0,names-corrected-line=0,stale-line=1,round35-lesson=1 closed=0
E9 payload=status-dirty=9,scratch-seat-dirs=0,head-match=0,lane-root=1,scratch-root=present closed=0
closed=3/9 exit=1
```
exit 1 — **3/9 on the r35 judged head export** (`<9/9`): E5/E6/E7 closed, E1/E2/E3/E4/E8/E9 open.
E2 is open there because that head still carries the stale `depth:density` row (no corrected
`201.2` row), which is why the erratum row is now a limb.

```
$ bash r36-closure.sh --export-ref b47f2cdf17d9f6021cbdb4db1add09a9dbf4f1d6 --scratch-root <empty>
export-ref=b47f2cdf17d9f6021cbdb4db1add09a9dbf4f1d6 mode=export lane=/home/vgpnk/Projects/shokunin/kasegi-shokunin suite-sha256=4db1ae70c76afd28b29e9ec24c2e44835322c61fa33e30c966f75ce0dfadb7c4
deviation=non-default --scratch-root
E1 payload=placeholders=0,lane-hash-markers=0,round36-section=0,round36-final-lane-commits=0,bound=0 closed=0
E2 payload=erratum-marker=1,erratum-row=1,erratum-mean=6 closed=1
E3 payload=registry-r35-defect-closure=0,registry-r36-closure=0 closed=0
E4 payload=tracked-ref=1,tracked-index=1,provenance-note=0 closed=0
E5 payload=claims-erratum-d5=1 closed=1
E6 payload=path=.ufo/waves/round-34/wave1/L1Integration.md,correction-round35=1 closed=1
E7 payload=supersedes-r22=1,supersedes-r23=1 closed=1
E8 payload=m36-rows=0,names-corrected-line=0,stale-line=0,round35-lesson=1 closed=0
E9 payload=status-dirty=9,scratch-seat-dirs=0,head-match=1,lane-root=1,scratch-root=present closed=0
closed=4/9 exit=1
```
exit 1 — 4/9 at the round-36 **claims-freeze** head; the open set is exactly the L1's remaining
landings (the round-36 SCORECARD section, E3 rows, E4 provenance note, E8 lesson, E9 quiescence).
`status-dirty=9` is the round-36 dispatch files plus the untracked `wave1/` receipts.

### Selftest at the frozen digest (HEAD export, empty `--scratch-root`)

```
selftest case=E1 positive=fail mutants=4/4 verdict=fail
selftest case=E2 positive=pass mutants=3/3 verdict=pass
selftest case=E3 positive=fail mutants=5/5 verdict=fail
selftest case=E4 positive=fail mutants=1/1 verdict=fail
selftest case=E5 positive=pass mutants=1/1 verdict=pass
selftest case=E6 positive=pass mutants=1/1 verdict=pass
selftest case=E7 positive=pass mutants=2/2 verdict=pass
selftest case=E8 positive=fail mutants=4/4 verdict=fail
selftest case=E9 positive=fail mutants=4/4 verdict=fail
selftest cases=9 failures=5
selftest judge=own-report accepted=0
selftest judge=forged-summary rejected=1
selftest judge=forged-caselines rejected=1
selftest judge=forged-failed-cases rejected=1
selftest judge=forged-detail-free rejected=1
```
exit 1. Nine cases executed; **every mutant rejected on its own reopened limb**:

| check | mutants (all rejected, limb named) |
|---|---|
| E1 | placeholder / lane-hash marker / unbound 40-hex (`bound=0`) / history-only, no round-36 section (`round36-section=0`) |
| E2 | stale mean (`erratum-mean=0`) / prose-only erratum (`erratum-row=0`) / erratum marker with no corrected row (`erratum-row=0`) |
| E3 | r36 row absent / r35 row absent / inexact basename / prose mention / row-shaped lines outside a registry section |
| E4 | provenance note absent |
| E5 | erratum file absent |
| E6 | `Correction (round 35)` absent |
| E7 | R23 row absent / prose instead of a row |
| E8 | `M36` absent / stale line present / corrected line unnamed / round-35 lesson absent |
| E9 | dirty worktree / leftover seat dir / stale ref / status repo inside an enclosing repo |

The five red positives are the five landings (E1's round-36 section included), so at the final head
this must read `selftest cases=9 failures=0` exit 0.

### Green-path proof (9/9 reachable)

Synthesized tree = `git archive` of HEAD + the four landings (a `## Round 36` SCORECARD section with
`**Final lane commit: `<HEAD>`**`, two `SKILL.md` registry rows inside a
`## Round-36 Gates & probes registry addition` section,
`.ufo/waves/round-35/wave1-results.json.provenance.md`, and `corpus/lessons/round-36.md` carrying
`M36` rows that name `source-recheck`), driven through the script's own check functions (sourcing is
supported: `main` runs only when `BASH_SOURCE[0] == $0`):

```
E1 rc=0 payload=placeholders=0,lane-hash-markers=0,round36-section=1,round36-final-lane-commits=1,bound=1
E2 rc=0 payload=erratum-marker=1,erratum-row=1,erratum-mean=6
E3 rc=0 payload=registry-r35-defect-closure=1,registry-r36-closure=1
E4 rc=0 payload=tracked-ref=1,tracked-index=1,provenance-note=1
E5 rc=0 payload=claims-erratum-d5=1
E6 rc=0 payload=path=.ufo/waves/round-34/wave1/L1Integration.md,correction-round35=1
E7 rc=0 payload=supersedes-r22=1,supersedes-r23=1
E8 rc=0 payload=m36-rows=2,names-corrected-line=1,stale-line=0,round35-lesson=1
E9 rc=0 payload=status-dirty=0,scratch-seat-dirs=0,head-match=1,lane-root=1,scratch-root=present
green_closed=9/9
```
E9's green limb used a clean one-commit fixture repo (toplevel verified equal to the fixture dir) as
`--lane`, an empty `--scratch-root`, and that repo's own HEAD. ExecC1ExportMode independently
measured `closed=9/9 exit=0` and `selftest cases=9 failures=0` on its all-green synthetic repo built
from the lane's full history (the stronger form: E1 then binds a real commit).

### Attacks and guards (measured)

| probe | result |
|---|---|
| E1, `Final lane commit` names a hash that exists but is **not an ancestor** (`8b26bc53…`) | rejected `round36-final-lane-commits=1,bound=0` |
| E1, a 64-hex sha256 where the 40-hex commit belongs | rejected `round36-final-lane-commits=0,bound=0` |
| E1, a bound line but **no round-36 section** (history only) | rejected `round36-section=0` |
| E1, lowercase `final lane commit` | accepted (matches `[Ff]inal`, as rounds 33/34 wrote it) |
| E1, prose placeholder `the L1 fills this line in the closing commit` | **passes** — measured, documented limit (same residue as the round-35 instrument) |
| E2, prose-only erratum (`## Round 36` + “the round-34 depth:density row was corrected… mean 201.2”) | rejected `erratum-row=0` |
| E3, both basenames in prose with the rows deleted (ExecC1Fixtures `mut-E3c`) | rejected (section-scoped row counter 0/0) |
| E3, both row-shaped lines under `## Cited paths` | rejected `registry-r36-closure=0` |
| E3, `| r35-defect-closure.sh.bak |` rows | rejected (cell must be the exact basename) |
| E7, a sentence quoting `supersedes R22/R23` | rejected `supersedes-r22=0` |
| E4, 0-byte provenance note beside `{}` results | rejected `provenance-note=0` |
| E5, 0-byte or directory `claims-erratum-d5.md` | rejected `claims-erratum-d5=0` |
| fabricated report: nine `case=E<i> … mutants=0/0 verdict=pass` lines + green summary (MutC1Fixtures) | rejected (`judge=forged-detail-free rejected=1`), no detail lines to cross-check |
| deleted-check attack (8-check copy) | `suite problem=self-report lines=8 expected=9`, `closed=0/9 exit=1` |
| stale bytes: pre-seed `<work>/export/.ufo/…/claims-erratum-d5.md`, run the base export | `E5=0`, `closed=0/9` — export cleared before extraction |
| `--work` inside the lane | exit 2 before `mkdir`; no directory created (verified) |
| relative `--lane` from another cwd | resolves to the absolute lane (printed in the header); E1 no longer a false red |
| no argument / unknown argument / missing value / unresolvable ref | exit 2 each with a named message |
| `TMPDIR=<scratch>/tmptest`, no `--work` | ran to completion, 0 leftovers |
| strace `-f -e openat,unlink` over a real-lane run | `index.lock=0`; zero absolute lane paths opened with write flags |
| export-mode purity at a fixed ref with a dirty worktree | E1–E8 payloads byte-stable; only E9's `status-dirty` moves |

## Documented limits (measured, not hidden)

- **E1** matches the two literal placeholder spellings named by the round-35 spot-check and this
  round's kill rule. The prose spelling passes (measured) — the round-35 instrument records the same
  residue; it is a checker-brittleness item, not a claimed-closed defect.
- **E4**'s `tracked-index` limb is the frozen `git ls-files` index read (mandated verbatim by the
  seat spec) and is ref-independent by nature; it is ANDed with the ref-scoped `ls-tree` limb.
- **E5** is a presence limb strengthened to “non-empty regular file”. The routed D5 statement
  clauses are deliberately not re-imposed.
- **E6** checks the appended `Correction (round 35)` marker only; a sentence that quotes the marker
  in a withdrawal (“the prior `Correction (round 35)` note was wrong…”) still passes. Textual markers
  cannot distinguish assertion from quotation; recorded rather than papered over.
- **E8** binds “a correction is recorded” through the `M36` rows, the named corrected instrument, the
  absence of the stale line in round-35 and that lesson's existence. It does **not** bind *what* the
  correction says: a lesson that keeps `source-recheck` and `M36` but drops the words “false
  evidence” or the `+10/0` measured pair still closes E8 (ExecC1Fixtures' E8b/E8d, measured at this
  digest). Those two are **documented survivors** of the “what was corrected” dimension, beyond the
  frozen limbs; the round-36 lesson should still say “false evidence” and quote the line.
- **Export symlinks.** The lane tree commits 58 symlinks whose targets are absolute live-lane
  paths; `git archive` preserves them. Every check reads explicit relative paths inside the export
  and the strace shows no reads through those links, so the export stays authoritative today — but a
  future *recursive* check would follow them into the live lane. Recorded as a constraint on any
  extension of this suite (ExecC1ExportMode observed it at the final digest).
- **E9** counts immediate child **directories** only (the frozen counter is `find … -type d`), so a
  stray regular file or a symlink at depth 1 does not move it; `scratch-root=present|absent` makes a
  typo'd or empty root visible without changing the frozen semantics. Historical exports can only be
  evaluated as “not quiescent now”; the staleness limb is what makes the negatives 0/9 and 3/9
  (removing it gives 1/9 and 4/9 on a quiescent machine).

## Deviations from `r35-defect-closure.sh` conventions (deliberate)

1. No `--root DIR` / live-tree mode — export mode plus `--selftest` only.
2. Check ids are the claim's `E1..E9`, not `D1..D7`.
3. Fixtures are generated per selftest case under `--work` instead of a committed fixture corpus:
   every limb is a one-line/one-row mutation of the live input, so the fixture is provably that
   input with one clause reopened, and the rejection must name the clause.
4. E9 carries the standing-`HEAD` limb and the lane-root limb; without the former the negatives are
   1/9 and 4/9, not 0/9 and `<9/9`; without the latter a status repo inside another repository would
   report that repository's cleanliness.
5. E1 is scoped to the round-36 SCORECARD block (a history-only closure is red), accepts `[Ff]inal`
   and binds every 40-hex in the window (stricter than the singular hash, fail-closed).
6. The self-report judgement re-parses the payload lines; the selftest judge requires nine executed
   cases, per-case detail lines matching `mutants=ok/n`, and rejects four forged reports.
7. `BASH_SOURCE` guard kept so the check functions can be driven directly by the green-path proof
   and review seats without a debug CLI mode. `run_check` folds its dispatch into
   `"check_${id,,}" "$@"`. The `forge-caselines` limb is kept because it is the literal
   claim-shaped forgery (`selftest cases=9 failures=0` with no case lines).

## Peer coordination (this wave)

- `ExecC1Fixtures` found the two clause-grain survivors that mattered (E3 satisfied by a mention, E8
  never checking that the lesson records the correction) plus the relative-`--lane` false red; all
  are fixed (section-scoped rows, named corrected line + lesson presence, lane normalisation), and
  their E5/E6 notes are recorded as limits. Their E8b/E8d are recorded as documented survivors.
- `ExecC1ExportMode` proved export-mode purity and found the one real lane write
  (`git status` taking `.git/index.lock`); fixed with `--no-optional-locks`, re-proved by my strace.
  It re-ran its full matrix on the FINAL bytes and returned **PASS at `4db1ae70`**: green
  `closed=9/9 exit=0` and `selftest cases=9 failures=0` (own report accepted, all four forgeries
  rejected) on a full-history synthetic repo; base `0/9`, judged `3/9`, real lane `4/9` with the
  same open set; 12 read-only git execve (no mutating subcommand), `tar -xf - -C <work>/export`,
  zero write syscalls and zero `index.lock` under both the synthetic repo and the real lane, lane
  `status` byte-equal with 6/6 read-file digests and `.git/index` size+mtime unchanged. Its
  committed-mutation canaries flip only E9 `head-match` (export at the old ref) or only E1
  `placeholders` (export at the mutated commit), which is the export-binding property the claim
  wants.
- `CritC1Kill`'s matrix produced the E1 history/quote survivors, the E2 prose survivor, the E4/E5
  empty-file survivals, the judge's detail-free forgery and the missing report binding; all six are
  repaired (round-36 scoping, erratum row+marker, `-s` limbs, detail cross-check, `lane=`/
  `suite-sha256=` header). Its E6 quote and E9 depth-1 notes are recorded as limits. It re-ran on
  the integrated digest, confirmed every repair by measurement, and produced twelve further
  fixtures; those are triaged one by one in **Post-integration residuals** below, and the eight that
  are worth a limb are the ordered round-37 backlog there. I did not modify the integrated bytes.
- `MutC1Fixtures` independently reproduced the detail-free judge forgery (`mutants=0/0` accepted) and
  the fx2 strength divergences; the judge now cross-checks detail lines and rejects it.
- `RevC1Suite` refused the first complete digest on E3/E7 (file-wide) and two vacuous edges, then
  re-reviewed and ADMITTED the repaired draft; its E1 fail-closed recommendation is kept.
- `ExecQuiescenceProbe` specified the same E9 recipe and the toplevel assertion that became
  `lane-root`.
- `SimplC1` proposed seven cuts; took the dispatch fold, the export-purity wording and the
  counterfactual correction, kept three with recorded reasons. Its third pass on the final bytes
  found no dead surface and one cosmetic duplication it explicitly did not think worth a freeze: the
  three-field banner (`export-ref`/`lane`/`suite-sha256` plus the optional `deviation=` lines) is
  printed in both `run_suite_report` and the selftest branch. Not taken: it is 3 lines of identical
  formatting over the same two functions (`suite_digest`, the override flags), a helper would only
  move the text, and the digest was already frozen and published to six seats when it was reported.
  Recorded so the next hand does not rediscover it as a defect.
- `ExecC1BaseFail` ran the negatives independently and independently found the missing round-35
  provenance note. `RevC1Suite-2`, `RevC1Selftest`, `MutC1Suite` were kept on the moving digest with
  the mutant inventory; `RevC1Suite-2`'s question about sibling-deletion is answered: every removal
  in the instrument is `$EXPORT`, `$MUT`, an auto-created `$WORK`, a `$MUT/<case>` fixture, or the
  fixture repo's `dirty.txt`; E9 only lists the scratch root.

## Post-integration residuals (recorded, deliberately not fixed)

CritC1Kill re-ran its matrix on the integrated digest (`4db1ae70`) and confirmed every earlier
repair by measurement, then produced twelve further fixtures that still read `closed=1` with the
mutation present. They were reported **after** the L1 integrated these bytes at `caa3146`; I did not
modify the committed instrument, because that would invalidate the L1's integration run and the
digest this receipt pins. ExecC1Fixtures' independent cross-run at the same digest reports "no
frozen-limb survivor" (10/14 clause mutants caught, the four survivors being E5b/E5c/E6b/E8b/E8d —
exactly this receipt's documented-limits set). Triage of the twelve, against the frozen claim's
wording rather than a stronger reading:

| # | fixture | why it closes today | frozen-limb verdict | hardening for round 37 |
|---|---|---|---|---|
| 1 | E1 names the round's **base** commit (`cc692008…`) on a `Final lane commit` line | it exists and is an ancestor, which is the frozen limb verbatim | conforms to the frozen wording; the kill rule's clause ("does not exist or is not an ancestor") is not triggered | accept only the export ref or its first parent (`ref`/`ref^1`) and add `on-head` to the payload |
| 2 | E1 decoy **last** `Round-36` heading carrying the bound line while the real section is empty | the hash line exists and binds; my scan takes the last matching heading | conforms (the decoy line is itself a valid closure line) | take the first matching heading, or the one inside the appended registry/closure block |
| 3 | E2 negated marker (`No Erratum (round 35) is owed.`) plus a fabricated corrected row | marker, row and mean are all present as text | the limb is "erratum present"; textual negation is not parseable | require the marker and the `round-34 depth:density row` anchor on ONE line, and restore r35 D2's stale-row (`mean **201.7**`) bytes limb — both are present at HEAD |
| 4 | E3 rows inside a `## …Gates & probes registry **retraction**…` section, type cell `not-a-probe` | my matcher accepts any heading containing the phrase and any row shape | a retraction section is not the registry home: this one does **not** conform | exclude headings matching `retract\|withdraw`, require the second cell to start `gate`/`probe` |
| 5 | E4 1-byte provenance note beside `{}` results | the limb is existence + non-empty | conforms (content is not in the claim) | require the note to name the results file (`wave1-results.json`) |
| 6 | E5 1-byte erratum | the limb is a non-empty regular file | conforms ("present") | restore r35 D5's `discriminating invocation` + `per-id occurrences` statements (both present 5× at HEAD) |
| 7 | E6 quoted **withdrawal** of the correction marker | the marker is present as text | conforms; recorded limit already | none that is textual; would need a content schema |
| 8 | E7 negation row (`| R30 | x | supersedes R22 is not needed … |`) | the third cell starts with the phrase | does **not** conform: a negation is not a supersession row | require the row's second cell to mention the same id (`R22`/`R23`) — both real rows do |
| 9 | E8 lesson = `M36 source-recheck` (two bare tokens), stale claim respelled in round-35 | both limbs are token/absence based | does **not** conform to "correction recorded" in spirit; conforms to my frozen-derived limbs | require `M36-[0-9]` and a quoted fragment of the corrected line in the round-36 lesson (the planned M36-2 row quotes it) |
| 10 | E9 leftover regular file / symlink at depth 1; or `--scratch-root <empty>` while the canonical root holds seat dirs | the frozen counter is `find … -type d`; the override prints `deviation=` but does not gate | the dirs-only reading conforms; the override case does **not** (the frozen measurement is the canonical root) | count any entry at depth 1 (report-only `scratch-files`), and make `exit=0` require a canonical scope (`scope=canonical`) while keeping overrides usable for per-check discrimination |
| 11 | fully fabricated report (nine case lines + nine `detail … mutant=forged rejected=1` lines) | shape-wise identical to a real report | out of reach of a text judge | only running the suite distinguishes execution from fabrication; the judge stays shape-based (as r35's) |
| 12 | fabricated `--lane` repo prints `closed=9/9` | `--lane` is honoured for review proofs | does **not** conform to the frozen command (canonical lane) | same scope gate as #10: `closed=9/9 exit=0` only when `lane` and `scratch-root` are canonical |

**Clause-4 disclosure (critic and I agree on this):** three of the twelve are kill-rule hits on the
integrated bytes, not limits — **#4 E3 retraction section**, **#8 E7 negation row**, **#9 E8 two bare
tokens**. RevC1Suite-2 independently refused on the E8 **negation** form (lesson
`no M36 rows minted; source-recheck unaffected`): reproduced here against the committed bytes, that
tree prints `E8 payload=m36-rows=1,names-corrected-line=1,stale-line=0,round35-lesson=1 closed=0`…
i.e. it closes, while the real lesson's `M36-1..4` rows are absent. The row-id regex below prints 0
on the negation and 4 on the real lesson, so the fix is one line. Each of these is a tree where the
check prints `closed=1` while the defect its clause names (unregistered / no supersession row /
correction not recorded) is present, so a judge using those fixtures could kill C1. They are disclosed here rather than folded into the limits list. #10/#12 are
invocation-scope only: the frozen counting command passes no `--lane`/`--scratch-root`, so a
non-canonical invocation is outside the claim's measurement (the `deviation=` line makes it visible).

**Measured after integration:** `caa3146` and `e666d90` read `closed=6/9` (E1 bound=0, E4 note=0,
E9 dirty); **`2c26a97` reads `closed=8/9 exit=1` with only E9 open** (`status-dirty=4`,
`scratch-seat-dirs=4`, `head-match=1`) — independently reproduced by me and by CritC1Kill. At that
head the round-36 line is `Final lane commit: e666d902…` (`SCORECARD.md:1492`) while HEAD is
`2c26a97`, so `bound=1` certifies "resolvable ancestor", exactly the frozen limb and not "the
closing commit" — the `on-head` limb is the first item of the round-37 backlog for that reason.
Only quiescence remains for `closed=9/9`.

Ordered round-37 backlog, by value: (a) E1 `on-head` (#1/#2), (b) E9/E12 canonical-scope gate that
makes a non-canonical run unable to print `exit=0` (#10/#12), (c) E3 retraction + type-cell (#4),
(d) E7 negation row (#8), (e) E8 `M36-[0-9]` + quoted line (#9), (f) E2 one-line statement + stale
row (#3), (g) E5 statement clauses (#6), (h) E4 note names the results file (#5). Each is a small,
independently testable limb; none was invented for this round's claim, which is why they are
recorded rather than retro-fitted after integration.

### v2 candidate — E8 row-id (tested, unlanded; the L1's decision)

Produced after integration in response to RevC1Suite-2's Major, measured, and **not landed**: the
committed instrument stays `4db1ae70` unless KasegiR36 says otherwise, because a re-cut changes the
digest five seats have pinned.

| field | value |
|---|---|
| v2 sha256 | `7f54f0e50023f5320fc889ffe44797c251db7eca849424df63f2eeff690467b7` |
| lines / bytes | 898 / 39 351 |
| diff vs `4db1ae70` | exactly two hunks: the `m36=` grep, and one selftest mutant |
| `bash -n` | exit 0 |

```diff
-    m36=$(grep -cF -- 'M36' corpus/lessons/round-36.md 2>/dev/null); m36=${m36:-0}
+    m36=$(grep -cE -- '(^|[^0-9A-Za-z])M36-[0-9]+([^0-9]|$)' corpus/lessons/round-36.md 2>/dev/null); m36=${m36:-0}
@@ selftest_case_E8 (after round35-lesson-absent)
+  n=$((n + 1)); d=$MUT/E8-negation; mut_reset "$d"
+  printf 'no M36 rows minted; source-recheck unaffected\n' | mut_put "$d" corpus/lessons/round-36.md
+  printf 'clean lesson\n' | mut_put "$d" corpus/lessons/round-35.md
+  st_neg E8 m36-negated "$d" "$REF_RESOLVED" 'm36-rows=0' && ok=$((ok + 1))
```

Measured on v2: base `3266c99` `closed=0/9 exit=1`; judged `0aee0ef` `closed=3/9 exit=1`; the then-current
lane head (`a23dc47`) `closed=8/9 exit=1` with only E9 open and `E8 payload=m36-rows=4,names-corrected-line=3,stale-line=0,round35-lesson=1 closed=1`;
`--selftest` `cases=9 failures=1` (only E9's positive, the pending quiescence), E1–E8 positives all pass,
E8 mutants 5/5 including `m36-negated rejected=1 limb=m36-rows=0`, four forgeries rejected. The real
lesson keeps 4 row matches; the negation fixture reads 0. Reproduce with the two hunks above against
the receipt's fenced block, then `sha256sum` must print `7f54f0e5…`.

Decision framing for the L1: landing it costs one commit and one re-run of the four counting
commands, and invalidates the digests pinned by five seats (ExportMode PASS, CritC1Kill close,
SimplC1, MutC1Fixtures, ExecC1Fixtures) — none of their *behavioural* results change, but their
receipts name `4db1ae70`. Not landing it leaves #9/RevC1Suite-2's Major disclosed as a clause-4 hit
with this patch as its fix. Either is defensible; the choice is the L1's, not mine.

## Files changed

- **Lane:** `.ufo/waves/round-36/wave1/ExecC1SuiteBuild.md` (this receipt) — the only lane write.
- **Scratch (removed at yield):** `/fast/scratch/hyaku/kasegi-r36/ExecC1SuiteBuild/` — the draft,
  the green-tree harness, the attack script, `empty-scratch`, probe snapshots, trace files.
- No lane source, no fleet root, no `shokuknow`, no sibling lane, no config/MCP file was touched.

## Draft text (verbatim, sha256 `4db1ae70c76afd28b29e9ec24c2e44835322c61fa33e30c966f75ce0dfadb7c4`, 894 lines)

```bash
#!/usr/bin/env bash
# r36-closure.sh — round-36 closure counter for claim C1 (depth:verifiability).
#
# Nine checks E1-E9, one per routed defect of the round-35 verifier spot-check
# plus the two standing closure-order defects. Each check exits 0 when its defect
# is CLOSED and non-zero while it is still OPEN, so the suite is a fail-closed
# gate over the bytes of a named lane head.
#
# EXPORT MODE IS THE ONLY RUN MODE. `--export-ref <hash>` extracts the lane tree
# with
#   git -C <lane> archive <hash> | tar -x -C <scratch>/export
# and every check reads its bytes only under that export root. The sole live
# reads are E9's quiescence limbs (worktree status, HEAD, scratch root) and E4's
# frozen `git ls-files` index limb, which are live by definition and cannot be
# answered from an export. A plain run (no --export-ref, no --selftest) refuses
# with exit 2, because a suite that reads the working tree can be turned green by
# edits that were never committed.
# The only ref-scoped git reads that cannot be answered from the export bytes —
# E1's commit existence/ancestry, E4's tracking lints, E9's quiescence — are
# read-only git subcommands against the lane repo (archive, rev-parse, cat-file
# -e, merge-base --is-ancestor, ls-tree, ls-files, status --porcelain; the status
# read runs with --no-optional-locks so it does not take .git/index.lock even
# transiently). Nothing is written under the lane; the only writes are the
# extraction and the selftest fixtures
# under --work (or a mktemp dir honouring TMPDIR), both removed on exit.
# --work must lie outside the lane; its `export/` and `mut/` subdirectories are
# cleared before use, so a reused work dir can never satisfy a check with stale
# bytes.
#
# Usage:
#   bash corpus/instruments/r36-closure.sh --export-ref <hash> [--lane DIR]
#        [--work DIR] [--scratch-root DIR]
#       Extract <hash> and run E1-E9 against the export. Prints one
#       `E<n> payload=<...> closed=0|1` line per check and a final
#       `closed=K/9 exit=0|1`; exit 0 only for K=9, exit 1 otherwise.
#   bash corpus/instruments/r36-closure.sh --selftest [--export-ref <hash>]
#        [--lane DIR] [--work DIR] [--scratch-root DIR]
#       Positive limb: every check must pass on the export (default: HEAD).
#       Mutant limb: for each check one or two scratch fixtures that reopen
#       exactly one clause of that check must be REJECTED, and the rejection
#       payload must name the reopened limb — so a fixture proves the check
#       discriminates rather than that it can be satisfied by a summary.
#       Prints one `selftest case=E<i> positive=... mutants=<ok>/<n> verdict=...`
#       line per check, the `selftest detail=` lines behind them, the
#       `selftest judge=` lines (own report accepted, three forged reports
#       rejected) and `selftest cases=9 failures=0`; exit 0 only when all nine
#       cases were executed, every positive passed and every mutant was rejected.
#   bash corpus/instruments/r36-closure.sh -h|--help
#       This text.
#
#   Plain run (no --export-ref, no --selftest) is refused: exit 2.
#
# The nine checks:
#   E1  Structural placeholder/hash binding. SCORECARD.md in the export carries
#       0 `filled by the L1` lines and 0 `<LANE_HASH>` marker lines, AND every
#       40-hex value on a `Final lane commit:` line (that line or the four lines
#       after it) exists as a commit in the lane repo and is an ancestor of the
#       exported ref. A closure that names a hash nobody can resolve, or names a
#       commit on a side branch, is not a binding.
#   E2  SCORECARD.md carries the round-34 depth:density erratum: the erratum
#       anchor `round-34 depth:density row` >= 1 AND the corrected mean `201.2`
#       >= 1 (the round-35 base carries 0 of each). The anchor limb is what keeps
#       a stray prose `201.2` elsewhere in SCORECARD.md from standing in for the
#       erratum row.
#   E3  SKILL.md registers BOTH closure instruments as registry ROWS by exact
#       basename at the Gates & probes registry home: the first table column
#       reads `r35-defect-closure.sh` (optional backticks) AND `r36-closure.sh`,
#       inside a `## …Gates & probes registry…` section (closed by the next
#       `## ` heading). A prose sentence that merely names them, or a row-shaped
#       line outside such a section, does not close this check — the round-35
#       spot-check's routed defect was a clause satisfied by mention or negation.
#   E4  `.ufo/waves/round-35/wave1-results.json` is tracked at the exported ref
#       (`ls-tree -r --name-only <ref> -- <path>` = 1 line) AND in the lane index
#       (the frozen `git ls-files` limb = 1 line) AND the provenance note
#       `<path>.provenance.md` exists in the export beside it.
#   E5  `.ufo/waves/round-35/claims-erratum-d5.md` exists in the export.
#   E6  The round-34 wave-1 integration receipt carries the appended
#       `Correction (round 35)` note. The receipt path is derived from the
#       export's own `ls-tree` listing (one candidate, fixture copies under
#       corpus/instruments/ excluded), not assumed.
#   E7  corpus/QUALITY.md carries both appended supersession ROWS: a table row
#       whose third column begins `supersedes R22` (>= 1) and the same for
#       `supersedes R23` (>= 1). A prose sentence quoting the row text does not
#       close the check.
#   E8  The round-36 lesson records the E8 correction: `M36` >= 1 rows in
#       corpus/lessons/round-36.md AND the corrected line is NAMED there
#       (`source-recheck` >= 1, so a lesson that never says what it corrected
#       fails) AND the false-evidence line is gone from
#       corpus/lessons/round-35.md (`source-recheck exit 0 on committed bytes`
#       == 0, and that lesson file must EXIST — an absent file does not read as
#       "stale line absent"). A lesson that keeps the stale evidence line fails
#       even when the new mistake rows are present.
#   E9  Quiescence. Four limbs: (a) the status repo IS the lane root
#       (`rev-parse --show-toplevel` equals its physical path — an export path or
#       a subdirectory inside another repository would otherwise inherit that
#       repo's cleanliness); (b) the lane worktree is clean
#       (`git status --porcelain` prints nothing); (c) the round-36 scratch root
#       has no leftover seat directories (`find <scratch-root> -mindepth 1
#       -maxdepth 1 -type d` empty, the suite's own --work dir excluded by
#       absolute path); (d) the exported ref IS the lane's standing HEAD
#       (`rev-parse HEAD`), so an export of a stale commit cannot read quiescent.
#       The payload also reports `scratch-root=present|absent`, so a typo'd
#       --scratch-root is visible rather than silently reading zero seats.
#       Limb (d) is the staleness guard: without it (measured by removing it on a
#       quiescent scratch root) the r35 base export reads 1/9 and the r35 judged
#       head 5/9, not the frozen 0/9 and the required <9/9.
#
# Documented limits (measured, not hidden):
#   - E1 matches the two placeholder spellings the round-35 spot-check and this
#     round's kill rule name literally. Prose placeholders ("the L1 fills this
#     line in") are not matched; the round-35 instrument records the same
#     residue and it is still open as a checker-brittleness item.
#   - E8 binds "correction recorded" through the `M36` mistake rows, the named
#     corrected instrument (`source-recheck`) and the removal of the stale line.
#     It does not require the lesson to quote the stale sentence verbatim,
#     because the correction's wording is the L1's.
#   - E9's limbs are live by construction (worktree, scratch root, HEAD). A
#     historical export can only be evaluated as "not quiescent now"; that is
#     the intended reading and the reason the negative controls are 0/9 and
#     <9/9 rather than "the old tree was clean when it was written".
#
# Exit codes: 0 closed / selftest clean, 1 open defect(s) / selftest failure,
# 2 harness error (unknown or missing argument, unresolvable ref, unreadable
# lane or export, archive failure). The plain-run refusal is exit 2.
set -uo pipefail

LANE=/home/vgpnk/Projects/shokunin/kasegi-shokunin
SCRATCH_ROOT=/fast/scratch/hyaku/kasegi-r36
CHECK_IDS=(E1 E2 E3 E4 E5 E6 E7 E8 E9)

MODE=run
EXPORT_REF=
WORK_ARG=
REF_RESOLVED=
WORK=
EXPORT=
MUT=
WORK_AUTO=0
LANE_OVERRIDE=0
SCRATCH_OVERRIDE=0
CASES=0
FAILS=0

# suite_digest — sha256 of the bytes actually executing, printed in the report so
# a reader can bind a `closed=9/9` line to the instrument that produced it.
suite_digest() {
  local s=${BASH_SOURCE[0]:-}
  if [ -n "$s" ] && [ -r "$s" ]; then
    sha256sum -- "$s" 2>/dev/null | awk '{print $1; exit}'
  else
    printf 'unreadable'
  fi
}

usage() {
  # the header block only: line 2 through the last comment line before the
  # option-less `set` line, so the help cannot drift from the docs.
  sed -n '2,/^set -uo pipefail$/p' "${BASH_SOURCE[0]}" | sed -e '$d' -e 's/^# \{0,1\}//'
}

die() { # MESSAGE...
  printf 'r36-closure: %s\n' "$*" >&2
  exit 2
}

parse_args() {
  while [ $# -gt 0 ]; do
    case $1 in
      --export-ref)
        [ $# -ge 2 ] || die '--export-ref needs a commit-ish'
        EXPORT_REF=$2; shift 2 ;;
      --work)
        [ $# -ge 2 ] || die '--work needs a directory'
        WORK_ARG=$2; shift 2 ;;
      --lane)
        [ $# -ge 2 ] || die '--lane needs a directory'
        LANE=$2; LANE_OVERRIDE=1; shift 2 ;;
      --scratch-root)
        [ $# -ge 2 ] || die '--scratch-root needs a directory'
        SCRATCH_ROOT=$2; SCRATCH_OVERRIDE=1; shift 2 ;;
      --selftest)
        MODE=selftest; shift ;;
      -h|--help)
        usage; exit 0 ;;
      *)
        printf 'r36-closure: unknown argument: %s\n' "$1" >&2
        usage >&2
        exit 2 ;;
    esac
  done
}

cleanup() {
  [ -n "${EXPORT:-}" ] && rm -rf -- "$EXPORT"
  [ -n "${MUT:-}" ] && rm -rf -- "$MUT"
  if [ "${WORK_AUTO:-0}" = 1 ] && [ -n "${WORK:-}" ]; then rm -rf -- "$WORK"; fi
}

make_work() {
  if [ -n "$WORK_ARG" ]; then
    # Guard BEFORE creating anything: a refused --work must leave no trace.
    local norm
    norm=$(realpath -m -- "$WORK_ARG" 2>/dev/null) \
      || die "cannot resolve work dir: $WORK_ARG"
    case $norm in
      "$LANE"|"$LANE"/*) die "--work must be outside the lane (it would write there): $norm" ;;
      /) die '--work must not be /' ;;
    esac
    mkdir -p -- "$norm" || die "cannot create work dir: $norm"
    WORK=$( cd "$norm" && pwd -P ) || die "cannot resolve work dir: $norm"
    # Re-check the physical path: a symlink may point into the lane.
    case $WORK in
      "$LANE"|"$LANE"/*) die "--work resolves inside the lane: $WORK" ;;
    esac
    WORK_AUTO=0
  else
    # TMPDIR is honoured by mktemp itself; no path is hardcoded here.
    WORK=$(mktemp -d -t r36-closure.XXXXXXXX) || die 'cannot create a work dir'
    WORK_AUTO=1
  fi
  EXPORT=$WORK/export
  MUT=$WORK/mut
  # Clear both owned subdirectories: a reused --work must never let a stale
  # export satisfy a check (e.g. an old claims-erratum-d5.md under export/).
  rm -rf -- "$EXPORT" "$MUT"
  mkdir -p -- "$EXPORT" "$MUT" || die "cannot populate work dir: $WORK"
  trap cleanup EXIT
}

prepare_export() {
  local want=${1:-$EXPORT_REF}
  [ -n "$want" ] || die 'export mode requires --export-ref <hash>'
  [ -d "$LANE" ] || die "lane is not a directory: $LANE"
  git -C "$LANE" rev-parse --git-dir >/dev/null 2>&1 \
    || die "lane is not a git repository: $LANE"
  REF_RESOLVED=$(git -C "$LANE" rev-parse --verify --quiet "${want}^{commit}") \
    || die "cannot resolve export ref in $LANE: $want"
  make_work
  git -C "$LANE" archive --format=tar "$REF_RESOLVED" | tar -xf - -C "$EXPORT" \
    || die "git archive export failed for $REF_RESOLVED"
  [ -f "$EXPORT/SCORECARD.md" ] \
    || die "export has no SCORECARD.md (not a lane tree): $REF_RESOLVED"
}

# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

# e1_final_hashes FILE — the 40-hex tokens on a `[Ff]inal lane commit` line (or
# in the four lines after it) inside the LAST `Round[- ]36` heading block. Scoping
# to the round-36 block is what stops the historical round-33/34/35 lines from
# satisfying the check: a closure section that carries no bound line is red.
# Splitting on non-hex runs keeps a 64-hex digest from being read as 40-hex.
e1_final_hashes() {
  awk '
    { line[NR] = $0 }
    END {
      start = 0
      for (i = 1; i <= NR; i++)
        if (line[i] ~ /^#{1,4} .*Round[- ]?36([^0-9]|$)/) start = i
      if (start == 0) exit
      for (i = start; i <= NR; i++) {
        if (line[i] ~ /[Ff]inal lane commit/) {
          for (j = i; j <= i + 4 && j <= NR; j++) {
            n = split(line[j], f, /[^0-9a-f]+/)
            for (k = 1; k <= n; k++) if (length(f[k]) == 40) print f[k]
          }
        }
      }
    }
  ' "$1" | sort -u
}

# e1_has_round36 FILE — 1 when SCORECARD.md carries a Round[- ]36 heading.
e1_has_round36() {
  awk '/^#{1,4} .*Round[- ]?36([^0-9]|$)/ { found = 1 } END { print found + 0 }' "$1"
}

# e3_registry_rows FILE BASENAME — count table rows whose first cell is exactly
# BASENAME (optional backticks), counting only inside a Gates & probes registry
# section (`## …Gates & probes registry…`, closed by the next `## ` heading).
# Section scoping is what stops a quoted row or a prose mention elsewhere in
# SKILL.md from satisfying the registry check.
e3_registry_rows() {
  awk -v name="$2" '
    BEGIN { b = name; gsub(/\./, "\\.", b); pat = "^\\|[[:space:]]*`?" b "`?[[:space:]]*\\|" }
    /^## / { inreg = ($0 ~ /Gates & probes registry/); next }
    inreg && $0 ~ pat { n++ }
    END { print n + 0 }
  ' "$1"
}

count_lines() { # reads stdin
  grep -c . 2>/dev/null || true
}

# ---------------------------------------------------------------------------
# checks — every one cd's into the export root and reads relative paths there
# ---------------------------------------------------------------------------

check_e1() { # TREE REF
  local tree=$1 ref=$2
  (
    cd "$tree" || { printf 'tree-unreadable'; exit 2; }
    [ -f SCORECARD.md ] || { printf 'scorecard-missing'; exit 1; }
    local ph lh section total=0 bound=0 h
    # Both placeholder literals are assembled so this instrument does not itself
    # contain the tokens it hunts for.
    ph=$(grep -cF -- "filled by the $(printf 'L1')" SCORECARD.md 2>/dev/null); ph=${ph:-0}
    lh=$(grep -cF -- "<LANE$(printf '_HASH')>" SCORECARD.md 2>/dev/null); lh=${lh:-0}
    section=$(e1_has_round36 SCORECARD.md); section=${section:-0}
    while IFS= read -r h; do
      [ -n "$h" ] || continue
      total=$((total + 1))
      if git -C "$LANE" cat-file -e "${h}^{commit}" 2>/dev/null \
         && git -C "$LANE" merge-base --is-ancestor "$h" "$ref" 2>/dev/null; then
        bound=$((bound + 1))
      fi
    done < <(e1_final_hashes SCORECARD.md)
    printf 'placeholders=%s,lane-hash-markers=%s,round36-section=%s,round36-final-lane-commits=%s,bound=%s' \
      "$ph" "$lh" "$section" "$total" "$bound"
    [ "$ph" -eq 0 ] && [ "$lh" -eq 0 ] && [ "$section" -eq 1 ] \
      && [ "$total" -ge 1 ] && [ "$bound" -eq "$total" ] && exit 0
    exit 1
  )
}

check_e2() { # TREE REF
  local tree=$1
  (
    cd "$tree" || { printf 'tree-unreadable'; exit 2; }
    local marker row mean
    # The erratum statement, the corrected depth:density row, and the corrected
    # mean. Requiring the marker and the row stops a prose sentence that quotes
    # the phrase or the number from standing in for the erratum.
    marker=$(grep -cF -- 'Erratum (round 35)' SCORECARD.md 2>/dev/null); marker=${marker:-0}
    row=$(grep -cE -- '^\|[[:space:]]*depth:density[[:space:]]*\|[[:space:]]*9[[:space:]]*\|[[:space:]]*mean \*\*201\.2\*\*' SCORECARD.md 2>/dev/null); row=${row:-0}
    mean=$(grep -cE -- '201\.2' SCORECARD.md 2>/dev/null); mean=${mean:-0}
    printf 'erratum-marker=%s,erratum-row=%s,erratum-mean=%s' "$marker" "$row" "$mean"
    [ "$marker" -ge 1 ] && [ "$row" -ge 1 ] && [ "$mean" -ge 1 ] && exit 0
    exit 1
  )
}

check_e3() { # TREE REF
  local tree=$1
  (
    cd "$tree" || { printf 'tree-unreadable'; exit 2; }
    local a b
    # Registry ROWS inside a Gates & probes registry section, not mentions: the
    # exact basename in the first table column (optional backticks). Round 35's
    # routed defect 3 was precisely "the clause greps are satisfied by a mention
    # or a negation", and the round-35 row named `r-defect-closure.sh`, the
    # round-33/34 instrument, which is why the exact basename is its own check.
    a=$(e3_registry_rows SKILL.md 'r35-defect-closure.sh')
    b=$(e3_registry_rows SKILL.md 'r36-closure.sh')
    printf 'registry-r35-defect-closure=%s,registry-r36-closure=%s' "$a" "$b"
    [ "$a" -ge 1 ] && [ "$b" -ge 1 ] && exit 0
    exit 1
  )
}

check_e4() { # TREE REF
  local tree=$1 ref=$2 p=.ufo/waves/round-35/wave1-results.json
  local t_ref t_idx note=0
  t_ref=$(git -C "$LANE" ls-tree -r --name-only "$ref" -- "$p" 2>/dev/null | count_lines)
  t_idx=$(git -C "$LANE" ls-files -- "$p" 2>/dev/null | count_lines)
  t_ref=${t_ref:-0}; t_idx=${t_idx:-0}
  if ( cd "$tree" && [ -f "$p.provenance.md" ] && [ -s "$p.provenance.md" ] ) 2>/dev/null; then note=1; fi
  printf 'tracked-ref=%s,tracked-index=%s,provenance-note=%s' "$t_ref" "$t_idx" "$note"
  [ "$t_ref" -eq 1 ] && [ "$t_idx" -eq 1 ] && [ "$note" -eq 1 ] && return 0
  return 1
}

check_e5() { # TREE REF
  local tree=$1
  (
    cd "$tree" || { printf 'tree-unreadable'; exit 2; }
    local p=.ufo/waves/round-35/claims-erratum-d5.md ok=0
    if [ -f "$p" ] && [ -s "$p" ]; then ok=1; fi
    printf 'claims-erratum-d5=%s' "$ok"
    [ "$ok" -eq 1 ] && exit 0
    exit 1
  )
}

check_e6() { # TREE REF
  local tree=$1 ref=$2
  local cand n path cor
  cand=$(git -C "$LANE" ls-tree -r --name-only "$ref" 2>/dev/null \
    | grep -E '(^|/)\.ufo/waves/round-34/wave1/L1Integration\.md$' \
    | grep -v '^corpus/instruments/')
  n=$(printf '%s\n' "$cand" | count_lines); n=${n:-0}
  if [ "$n" -ne 1 ]; then
    printf 'path-candidates=%s,correction-round35=0' "$n"
    return 1
  fi
  path=$cand
  cor=$( ( cd "$tree" && grep -cF -- 'Correction (round 35)' "$path" 2>/dev/null ) || true )
  cor=${cor:-0}
  printf 'path=%s,correction-round35=%s' "$path" "$cor"
  [ "$cor" -ge 1 ] && return 0
  return 1
}

check_e7() { # TREE REF
  local tree=$1
  (
    cd "$tree" || { printf 'tree-unreadable'; exit 2; }
    local r22 r23
    # Rows, not prose: the third column of a QUALITY.md row begins with the
    # supersession statement. A sentence that mentions the row text must not
    # close the check (round-35 routed defect 3/D7 class).
    r22=$(grep -cE -- '^\|[[:space:]]*R[0-9]+[[:space:]]*\|[^|]*\|[[:space:]]*supersedes R22($|[^0-9])' corpus/QUALITY.md 2>/dev/null); r22=${r22:-0}
    r23=$(grep -cE -- '^\|[[:space:]]*R[0-9]+[[:space:]]*\|[^|]*\|[[:space:]]*supersedes R23($|[^0-9])' corpus/QUALITY.md 2>/dev/null); r23=${r23:-0}
    printf 'supersedes-r22=%s,supersedes-r23=%s' "$r22" "$r23"
    [ "$r22" -ge 1 ] && [ "$r23" -ge 1 ] && exit 0
    exit 1
  )
}

check_e8() { # TREE REF
  local tree=$1
  (
    cd "$tree" || { printf 'tree-unreadable'; exit 2; }
    local m36 names stale=0 lesson35=0
    m36=$(grep -cF -- 'M36' corpus/lessons/round-36.md 2>/dev/null); m36=${m36:-0}
    # The correction must NAME the line it corrects: the round-36 lesson has to
    # mention the instrument whose output was the false evidence line. "Rows
    # exist" alone would close the check while the lesson never records what it
    # corrected.
    names=$(grep -cF -- 'source-recheck' corpus/lessons/round-36.md 2>/dev/null); names=${names:-0}
    # The absence limb is only meaningful when the lesson it applies to exists;
    # a missing round-35 lesson must not read as "stale line absent".
    if [ -f corpus/lessons/round-35.md ]; then
      lesson35=1
      stale=$(grep -cF -- 'source-recheck exit 0 on committed bytes' \
        corpus/lessons/round-35.md 2>/dev/null); stale=${stale:-0}
    fi
    printf 'm36-rows=%s,names-corrected-line=%s,stale-line=%s,round35-lesson=%s' \
      "$m36" "$names" "$stale" "$lesson35"
    [ "$m36" -ge 1 ] && [ "$names" -ge 1 ] && [ "$stale" -eq 0 ] \
      && [ "$lesson35" -eq 1 ] && exit 0
    exit 1
  )
}

check_e9() { # TREE REF [SCRATCH_ROOT [STATUS_REPO [EXPECTED_HEAD]]]
  local ref=$2
  local sroot=${3:-$SCRATCH_ROOT}
  local srepo=${4:-$LANE}
  local want=${5:-$ref}
  local porcelain left=0 head head_ok=0 root_ok=0 skip= d dp top root sroot_state=absent
  if ! git -C "$srepo" rev-parse --git-dir >/dev/null 2>&1; then
    printf 'status-repo=unreadable,scratch-seat-dirs=?,head-match=0,lane-root=0,scratch-root=?'
    return 1
  fi
  # The status repo must BE the lane root: an export path or a subdirectory of
  # some enclosing repository would otherwise report another tree's cleanliness.
  root=$( cd "$srepo" 2>/dev/null && pwd -P )
  top=$(git -C "$srepo" rev-parse --show-toplevel 2>/dev/null)
  if [ -n "$top" ] && [ -n "$root" ] && [ "$top" = "$root" ]; then root_ok=1; fi
  # --no-optional-locks: plain `git status` takes and unlinks .git/index.lock,
  # a transient write under the lane. This suite must leave the lane untouched.
  porcelain=$(git --no-optional-locks -C "$srepo" status --porcelain 2>/dev/null | count_lines)
  porcelain=${porcelain:-0}
  if [ -n "${WORK:-}" ]; then skip=$( cd "$WORK" 2>/dev/null && pwd -P ); fi
  if [ -d "$sroot" ]; then
    sroot_state=present
    while IFS= read -r d; do
      [ -n "$d" ] || continue
      dp=$( cd "$d" 2>/dev/null && pwd -P )
      if [ -n "$skip" ] && [ "$dp" = "$skip" ]; then continue; fi
      left=$((left + 1))
    done < <(find "$sroot" -mindepth 1 -maxdepth 1 -type d 2>/dev/null)
  fi
  head=$(git -C "$srepo" rev-parse --verify --quiet HEAD 2>/dev/null)
  if [ -n "$head" ] && [ "$head" = "$want" ]; then head_ok=1; fi
  printf 'status-dirty=%s,scratch-seat-dirs=%s,head-match=%s,lane-root=%s,scratch-root=%s' \
    "$porcelain" "$left" "$head_ok" "$root_ok" "$sroot_state"
  [ "$porcelain" -eq 0 ] && [ "$left" -eq 0 ] && [ "$head_ok" -eq 1 ] \
    && [ "$root_ok" -eq 1 ] && return 0
  return 1
}

run_check() { # ID TREE REF [EXTRA...]
  local id=$1; shift
  # one name derivation instead of a second registry beside CHECK_IDS
  "check_${id,,}" "$@"
}

# ---------------------------------------------------------------------------
# plain (export) run
# ---------------------------------------------------------------------------

run_suite_report() {
  local lines='' id out rc k=0 n=0 counted=0
  printf 'export-ref=%s mode=export lane=%s suite-sha256=%s\n' \
    "$REF_RESOLVED" "$LANE" "$(suite_digest)"
  if [ "$LANE_OVERRIDE" -eq 1 ]; then printf 'deviation=non-default --lane\n'; fi
  if [ "$SCRATCH_OVERRIDE" -eq 1 ]; then printf 'deviation=non-default --scratch-root\n'; fi
  for id in "${CHECK_IDS[@]}"; do
    out=$(run_check "$id" "$EXPORT" "$REF_RESOLVED" 2>/dev/null); rc=$?
    if [ "$rc" -eq 0 ]; then
      k=$((k + 1))
      lines="${lines}${id} payload=${out} closed=1"$'\n'
    else
      lines="${lines}${id} payload=${out} closed=0"$'\n'
    fi
  done
  printf '%s' "$lines"
  n=$(printf '%s' "$lines" | grep -c '^E[1-9] payload=')
  if [ "$n" -ne 9 ]; then
    printf 'suite problem=self-report lines=%s expected=9\n' "$n"
    printf 'closed=0/9 exit=1\n'
    return 1
  fi
  counted=$(printf '%s' "$lines" | grep -c 'closed=1$')
  if [ "$counted" -ne "$k" ]; then
    printf 'suite problem=self-report closed=%s counted=%s\n' "$k" "$counted"
    printf 'closed=0/9 exit=1\n'
    return 1
  fi
  if [ "$k" -eq 9 ]; then
    printf 'closed=%s/9 exit=0\n' "$k"
    return 0
  fi
  printf 'closed=%s/9 exit=1\n' "$k"
  return 1
}

# ---------------------------------------------------------------------------
# selftest fixtures
# ---------------------------------------------------------------------------

mut_reset() { # DIR
  rm -rf -- "$1"
  mkdir -p -- "$1"
}

mut_put() { # DIR RELPATH (stdin)
  mkdir -p -- "$1/$(dirname -- "$2")"
  cat > "$1/$2"
}

st_pos() { # ID TREE REF
  local id=$1 out rc
  out=$(run_check "$id" "$2" "$3" 2>/dev/null); rc=$?
  if [ "$rc" -eq 0 ]; then
    printf 'selftest detail=%s positive=pass payload=%s\n' "$id" "$out"
    return 0
  fi
  printf 'selftest detail=%s positive=fail rc=%s payload=%s\n' "$id" "$rc" "$out"
  return 1
}

st_neg() { # ID LABEL TREE REF NEEDLE [EXTRA...]
  local id=$1 label=$2 tree=$3 ref=$4 needle=$5; shift 5
  local out rc
  out=$(run_check "$id" "$tree" "$ref" "$@" 2>/dev/null); rc=$?
  if [ "$rc" -ne 0 ] && printf '%s' "$out" | grep -qF -- "$needle"; then
    printf 'selftest detail=%s mutant=%s rejected=1 limb=%s\n' "$id" "$label" "$needle"
    return 0
  fi
  printf 'selftest detail=%s mutant=%s rejected=0 rc=%s payload=%s\n' \
    "$id" "$label" "$rc" "$out"
  return 1
}

st_verdict() { # ID BAD OK N
  local id=$1 bad=$2 ok=$3 n=$4
  if [ "$bad" -eq 0 ] && [ "$n" -ge 1 ] && [ "$ok" -eq "$n" ]; then
    printf 'selftest case=%s positive=pass mutants=%s/%s verdict=pass\n' "$id" "$ok" "$n"
    return 0
  fi
  printf 'selftest case=%s positive=%s mutants=%s/%s verdict=fail\n' \
    "$id" "$([ "$bad" -eq 0 ] && echo pass || echo fail)" "$ok" "$n"
  FAILS=$((FAILS + 1))
  return 1
}

selftest_case_E1() {
  local bad=0 ok=0 n=0 h d
  CASES=$((CASES + 1))
  st_pos E1 "$EXPORT" "$REF_RESOLVED" || bad=1
  h=$(e1_final_hashes "$EXPORT/SCORECARD.md" | head -n 1)
  [ -n "$h" ] || h=$REF_RESOLVED
  n=$((n + 1)); d=$MUT/E1-placeholder; mut_reset "$d"
  printf '## Round 36\n\n**Final lane commit: `%s`**\nfilled by the %s\n' "$h" 'L1' \
    | mut_put "$d" SCORECARD.md
  st_neg E1 placeholder "$d" "$REF_RESOLVED" 'placeholders=1' && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/E1-lanehash; mut_reset "$d"
  printf '## Round 36\n\n**Final lane commit: `%s`**\n<%s>\n' "$h" 'LANE_HASH' \
    | mut_put "$d" SCORECARD.md
  st_neg E1 lane-hash-marker "$d" "$REF_RESOLVED" 'lane-hash-markers=1' && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/E1-unbound; mut_reset "$d"
  printf '## Round 36\n\n**Final lane commit: `%s`**\n' \
    '0123456789abcdef0123456789abcdef01234567' | mut_put "$d" SCORECARD.md
  st_neg E1 unbound-hash "$d" "$REF_RESOLVED" 'bound=0' && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/E1-history; mut_reset "$d"
  printf '**Final lane commit: `%s`**\n' "$h" | mut_put "$d" SCORECARD.md
  st_neg E1 history-only "$d" "$REF_RESOLVED" 'round36-section=0' && ok=$((ok + 1))
  st_verdict E1 "$bad" "$ok" "$n"
}

selftest_case_E2() {
  local bad=0 ok=0 n=0 d
  CASES=$((CASES + 1))
  st_pos E2 "$EXPORT" "$REF_RESOLVED" || bad=1
  n=$((n + 1)); d=$MUT/E2; mut_reset "$d"
  printf '| depth:density | 9 | mean **201.7**, 25 blocks |\n' | mut_put "$d" SCORECARD.md
  st_neg E2 stale-mean "$d" "$REF_RESOLVED" 'erratum-mean=0' && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/E2-prose; mut_reset "$d"
  printf '## Round 36\n\nNote: the round-34 depth:density row was corrected last round; guard mean 201.2.\n' \
    | mut_put "$d" SCORECARD.md
  st_neg E2 prose-not-row "$d" "$REF_RESOLVED" 'erratum-row=0' && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/E2-marker; mut_reset "$d"
  printf 'Erratum (round 35): the depth:density mean is 201.2, corrected.\n' \
    | mut_put "$d" SCORECARD.md
  st_neg E2 marker-without-row "$d" "$REF_RESOLVED" 'erratum-row=0' && ok=$((ok + 1))
  st_verdict E2 "$bad" "$ok" "$n"
}

selftest_case_E3() {
  local bad=0 ok=0 n=0 d
  CASES=$((CASES + 1))
  st_pos E3 "$EXPORT" "$REF_RESOLVED" || bad=1
  n=$((n + 1)); d=$MUT/E3-r35only; mut_reset "$d"
  printf '| r35-defect-closure.sh | gate | bash ... |\n' | mut_put "$d" SKILL.md
  st_neg E3 r36-row-absent "$d" "$REF_RESOLVED" 'registry-r36-closure=0' && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/E3-r36only; mut_reset "$d"
  printf '| r36-closure.sh | gate | bash ... |\n' | mut_put "$d" SKILL.md
  st_neg E3 r35-row-absent "$d" "$REF_RESOLVED" 'registry-r35-defect-closure=0' && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/E3-inexact; mut_reset "$d"
  printf '| r-defect-closure.sh | gate | bash ... |\n| r36-closure.sh | gate | bash ... |\n' \
    | mut_put "$d" SKILL.md
  st_neg E3 inexact-basename "$d" "$REF_RESOLVED" 'registry-r35-defect-closure=0' && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/E3-mention; mut_reset "$d"
  printf 'The gate later reads r36-closure.sh and r35-defect-closure.sh.\n' \
    | mut_put "$d" SKILL.md
  st_neg E3 mention-not-row "$d" "$REF_RESOLVED" 'registry-r36-closure=0' && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/E3-outside; mut_reset "$d"
  printf '## Cited paths\n\n| r35-defect-closure.sh | gate | x |\n| r36-closure.sh | gate | x |\n' \
    | mut_put "$d" SKILL.md
  st_neg E3 rows-outside-registry "$d" "$REF_RESOLVED" 'registry-r36-closure=0' && ok=$((ok + 1))
  st_verdict E3 "$bad" "$ok" "$n"
}

selftest_case_E4() {
  local bad=0 ok=0 n=0 d
  CASES=$((CASES + 1))
  st_pos E4 "$EXPORT" "$REF_RESOLVED" || bad=1
  n=$((n + 1)); d=$MUT/E4; mut_reset "$d"
  printf '{"wave": 1}\n' | mut_put "$d" .ufo/waves/round-35/wave1-results.json
  st_neg E4 provenance-absent "$d" "$REF_RESOLVED" 'provenance-note=0' && ok=$((ok + 1))
  st_verdict E4 "$bad" "$ok" "$n"
}

selftest_case_E5() {
  local bad=0 ok=0 n=0 d
  CASES=$((CASES + 1))
  st_pos E5 "$EXPORT" "$REF_RESOLVED" || bad=1
  n=$((n + 1)); d=$MUT/E5; mut_reset "$d"
  printf 'no erratum here\n' | mut_put "$d" README.md
  st_neg E5 erratum-absent "$d" "$REF_RESOLVED" 'claims-erratum-d5=0' && ok=$((ok + 1))
  st_verdict E5 "$bad" "$ok" "$n"
}

selftest_case_E6() {
  local bad=0 ok=0 n=0 d
  CASES=$((CASES + 1))
  st_pos E6 "$EXPORT" "$REF_RESOLVED" || bad=1
  n=$((n + 1)); d=$MUT/E6; mut_reset "$d"
  printf 'Correction (round 34) only.\n' \
    | mut_put "$d" .ufo/waves/round-34/wave1/L1Integration.md
  st_neg E6 correction-absent "$d" "$REF_RESOLVED" 'correction-round35=0' && ok=$((ok + 1))
  st_verdict E6 "$bad" "$ok" "$n"
}

selftest_case_E7() {
  local bad=0 ok=0 n=0 d
  CASES=$((CASES + 1))
  st_pos E7 "$EXPORT" "$REF_RESOLVED" || bad=1
  n=$((n + 1)); d=$MUT/E7; mut_reset "$d"
  printf '| R26 | ... | supersedes R22 - grounding fixed. |\n' | mut_put "$d" corpus/QUALITY.md
  st_neg E7 r23-row-absent "$d" "$REF_RESOLVED" 'supersedes-r23=0' && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/E7-prose; mut_reset "$d"
  printf 'Note: this row supersedes R22 and supersedes R23 in spirit.\n' \
    | mut_put "$d" corpus/QUALITY.md
  st_neg E7 prose-not-row "$d" "$REF_RESOLVED" 'supersedes-r22=0' && ok=$((ok + 1))
  st_verdict E7 "$bad" "$ok" "$n"
}

selftest_case_E8() {
  local bad=0 ok=0 n=0 d
  CASES=$((CASES + 1))
  st_pos E8 "$EXPORT" "$REF_RESOLVED" || bad=1
  n=$((n + 1)); d=$MUT/E8-nom36; mut_reset "$d"
  printf 'round 36 lesson without the mistake rows\n' | mut_put "$d" corpus/lessons/round-36.md
  printf 'clean lesson\n' | mut_put "$d" corpus/lessons/round-35.md
  st_neg E8 m36-absent "$d" "$REF_RESOLVED" 'm36-rows=0' && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/E8-stale; mut_reset "$d"
  printf 'M36-1 source-recheck false line corrected here\n' | mut_put "$d" corpus/lessons/round-36.md
  printf 'gate says source-recheck exit 0 on committed bytes\n' | mut_put "$d" corpus/lessons/round-35.md
  st_neg E8 stale-line-present "$d" "$REF_RESOLVED" 'stale-line=1' && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/E8-unnamed; mut_reset "$d"
  printf 'M36-1 correction recorded: the stale evidence line is withdrawn\n' \
    | mut_put "$d" corpus/lessons/round-36.md
  printf 'clean lesson\n' | mut_put "$d" corpus/lessons/round-35.md
  st_neg E8 corrected-line-unnamed "$d" "$REF_RESOLVED" 'names-corrected-line=0' && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/E8-nolesson35; mut_reset "$d"
  printf 'M36-1 source-recheck false line corrected here\n' | mut_put "$d" corpus/lessons/round-36.md
  st_neg E8 round35-lesson-absent "$d" "$REF_RESOLVED" 'round35-lesson=0' && ok=$((ok + 1))
  st_verdict E8 "$bad" "$ok" "$n"
}

selftest_case_E9() {
  local bad=0 ok=0 n=0 repo sroot top real head
  CASES=$((CASES + 1))
  st_pos E9 "$EXPORT" "$REF_RESOLVED" || bad=1
  repo=$MUT/e9repo; sroot=$MUT/e9scratch
  mut_reset "$repo"; mut_reset "$sroot"
  if ! git -C "$repo" init -q 2>/dev/null; then
    printf 'selftest detail=E9 fixture=repo-init-failed\n'; FAILS=$((FAILS + 1)); return
  fi
  top=$(git -C "$repo" rev-parse --show-toplevel 2>/dev/null)
  real=$( cd "$repo" && pwd -P )
  if [ "$top" != "$real" ]; then
    printf 'selftest detail=E9 fixture=toplevel-mismatch top=%s want=%s\n' "$top" "$real"
    FAILS=$((FAILS + 1)); return
  fi
  printf 'x\n' > "$repo/tracked.txt"
  git -C "$repo" add -- tracked.txt 2>/dev/null
  git -C "$repo" -c user.email=r36@local -c user.name=r36 commit -q -m fixture 2>/dev/null
  head=$(git -C "$repo" rev-parse --verify HEAD 2>/dev/null)
  printf 'untracked\n' > "$repo/dirty.txt"
  n=$((n + 1))
  st_neg E9 dirty-worktree "$EXPORT" "$REF_RESOLVED" 'status-dirty=1' \
    "$sroot" "$repo" "$head" && ok=$((ok + 1))
  rm -f -- "$repo/dirty.txt"
  mkdir -p -- "$sroot/leftover-seat"
  n=$((n + 1))
  st_neg E9 leftover-seat-dir "$EXPORT" "$REF_RESOLVED" 'scratch-seat-dirs=1' \
    "$sroot" "$repo" "$head" && ok=$((ok + 1))
  n=$((n + 1))
  mut_reset "$MUT/e9scratch-empty"
  st_neg E9 stale-ref "$EXPORT" "$REF_RESOLVED" 'head-match=0' \
    "$MUT/e9scratch-empty" "$repo" "0000000000000000000000000000000000000000" \
    && ok=$((ok + 1))
  # a status repo that is a subdirectory of an enclosing repo: cleanliness and
  # HEAD would be inherited from the parent, so the lane-root limb must reject it
  mkdir -p -- "$repo/sub"
  n=$((n + 1))
  st_neg E9 enclosing-repo "$EXPORT" "$REF_RESOLVED" 'lane-root=0' \
    "$sroot" "$repo/sub" "$head" && ok=$((ok + 1))
  st_verdict E9 "$bad" "$ok" "$n"
}

# ---------------------------------------------------------------------------
# selftest report judgement — a summary line alone must never pass
# ---------------------------------------------------------------------------

judge_selftest_report() { # FILE
  local f=$1 cases verdicts summary id hit=0 line n ok det rej
  [ -f "$f" ] || return 1
  cases=$(grep -c '^selftest case=' "$f" 2>/dev/null); cases=${cases:-0}
  verdicts=$(grep -c '^selftest case=.*verdict=pass$' "$f" 2>/dev/null); verdicts=${verdicts:-0}
  summary=$(grep -c '^selftest cases=9 failures=0$' "$f" 2>/dev/null); summary=${summary:-0}
  [ "$cases" -eq 9 ] && [ "$verdicts" -eq 9 ] && [ "$summary" -eq 1 ] || return 1
  # Every check id appears exactly once as a passing case line, and that line's
  # mutants=<ok>/<n> must be matched by exactly n `selftest detail=E<i> mutant=`
  # lines of which ok name rejected=1. A fabricated case line carrying
  # `mutants=0/0` (no fixture ran) is rejected: n must be >= 1 and the detail
  # lines must exist. This is the round-35 report_ok rule.
  for id in "${CHECK_IDS[@]}"; do
    line=$(grep -m1 "^selftest case=${id} " "$f" 2>/dev/null)
    [ -n "$line" ] || return 1
    printf '%s' "$line" | grep -q "verdict=pass$" || return 1
    n=$(printf '%s' "$line" | sed -n 's/.*mutants=[0-9][0-9]*\/\([0-9][0-9]*\).*/\1/p')
    ok=$(printf '%s' "$line" | sed -n 's/.*mutants=\([0-9][0-9]*\)\/[0-9][0-9]*.*/\1/p')
    [ -n "$n" ] && [ -n "$ok" ] && [ "$n" -ge 1 ] || return 1
    det=$(grep -c "^selftest detail=${id} mutant=" "$f" 2>/dev/null); det=${det:-0}
    rej=$(grep -c "^selftest detail=${id} mutant=.*rejected=1" "$f" 2>/dev/null); rej=${rej:-0}
    [ "$det" -eq "$n" ] && [ "$rej" -eq "$ok" ] && [ "$ok" -eq "$n" ] || return 1
    hit=$((hit + 1))
  done
  [ "$hit" -eq 9 ]
}

run_selftest() {
  local f=$WORK/selftest-report.txt rc=0 id
  {
    for id in "${CHECK_IDS[@]}"; do
      "selftest_case_${id}"
    done
    printf 'selftest cases=%s failures=%s\n' "$CASES" "$FAILS"
  } > "$f" 2>&1
  cat "$f"

  if judge_selftest_report "$f"; then
    printf 'selftest judge=own-report accepted=1\n'
  else
    printf 'selftest judge=own-report accepted=0\n'
    rc=1
  fi

  printf 'selftest cases=0 failures=0\n' > "$WORK/forge-summary.txt"
  if judge_selftest_report "$WORK/forge-summary.txt"; then
    printf 'selftest judge=forged-summary rejected=0\n'; rc=1
  else
    printf 'selftest judge=forged-summary rejected=1\n'
  fi

  printf 'selftest cases=9 failures=0\n' > "$WORK/forge-caselines.txt"
  if judge_selftest_report "$WORK/forge-caselines.txt"; then
    printf 'selftest judge=forged-caselines rejected=0\n'; rc=1
  else
    printf 'selftest judge=forged-caselines rejected=1\n'
  fi

  {
    local i
    for i in 1 2 3 4 5 6 7 8 9; do
      printf 'selftest case=E%s positive=fail mutants=0/1 verdict=fail\n' "$i"
    done
    printf 'selftest cases=9 failures=0\n'
  } > "$WORK/forge-failed-cases.txt"
  if judge_selftest_report "$WORK/forge-failed-cases.txt"; then
    printf 'selftest judge=forged-failed-cases rejected=0\n'; rc=1
  else
    printf 'selftest judge=forged-failed-cases rejected=1\n'
  fi

  # the detail-free all-pass forgery: nine case lines claiming pass with
  # mutants=0/0 and no fixture detail behind them (MutC1Fixtures' vacuous report)
  {
    local i
    for i in 1 2 3 4 5 6 7 8 9; do
      printf 'selftest case=E%s positive=pass mutants=0/0 verdict=pass\n' "$i"
    done
    printf 'selftest cases=9 failures=0\n'
  } > "$WORK/forge-detail-free.txt"
  if judge_selftest_report "$WORK/forge-detail-free.txt"; then
    printf 'selftest judge=forged-detail-free rejected=0\n'; rc=1
  else
    printf 'selftest judge=forged-detail-free rejected=1\n'
  fi

  if [ "$CASES" -ne 9 ]; then
    printf 'selftest problem=cases=%s expected=9\n' "$CASES"
    rc=1
  fi
  [ "$FAILS" -eq 0 ] || rc=1
  return "$rc"
}

# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

main() {
  parse_args "$@"
  # Normalise the lane once: every later `git -C "$LANE"` then works from any
  # cwd (a relative --lane used to resolve against the export tree inside E1's
  # subshell and read a false red).
  [ -d "$LANE" ] || die "lane is not a directory: $LANE"
  LANE=$( cd "$LANE" && pwd -P ) || die "cannot resolve lane: $LANE"
  case $MODE in
    run)
      if [ -z "$EXPORT_REF" ]; then
        printf 'r36-closure: refusing to run against the live worktree: this suite is export-mode only.\n' >&2
        printf 'r36-closure: pass --export-ref <hash> (see --help) or --selftest.\n' >&2
        exit 2
      fi
      prepare_export "$EXPORT_REF"
      run_suite_report
      ;;
    selftest)
      prepare_export "${EXPORT_REF:-HEAD}"
      printf 'selftest export-ref=%s lane=%s suite-sha256=%s\n' \
        "$REF_RESOLVED" "$LANE" "$(suite_digest)"
      if [ "$LANE_OVERRIDE" -eq 1 ]; then printf 'deviation=non-default --lane\n'; fi
      if [ "$SCRATCH_OVERRIDE" -eq 1 ]; then printf 'deviation=non-default --scratch-root\n'; fi
      run_selftest
      ;;
    *)
      die "unknown mode: $MODE"
      ;;
  esac
}

if [ "${BASH_SOURCE[0]}" = "$0" ]; then
  main "$@"
fi
```
