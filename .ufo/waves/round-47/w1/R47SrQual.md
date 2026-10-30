# R47SrQual — QUALITY.md round-47 additions block draft (R54, R55)

Seat R47SrQual (scribe), kasegi wave 1, 2026-10-30. Item: draft the round-47 additions
block for `corpus/QUALITY.md` in R6 form — every existing line keeps its number, the block
appends after the round-46 additions block; two criteria mined from THIS round's mistakes
(R54 from the D5 mine, R55 from the D7 mine), each grounded in a round-47 lesson row, one
paragraph, no scope creep. Byte figures below are draft-time placeholders the L1 re-measures
at landing (R19 stale-premise rule). No lane file outside `.ufo/waves/round-47/w1/` is
written; nothing is committed.

## Draft-time measurements (placeholders; L1 re-runs both commands immediately before writing)

- Tree: lane HEAD `82a8bd702900889c70a8fc2dbae91d2095dec800` (`git rev-parse HEAD`); freeze
  commit `308a2cb2` precedes it and does not touch `corpus/QUALITY.md` (freeze carries only
  instruments, captures/manifest, claims, controls — claims.json C1 `freeze_tree_reading`);
  `git status --porcelain -- corpus/QUALITY.md` printed empty, so the bytes below are the
  bytes both trees serve.
- `wc -c corpus/QUALITY.md` → `88671`; `wc -l` → `393`;
  `head -c 88671 corpus/QUALITY.md | sha256sum` →
  `95a09d5d375da260086181cc8207dc3341129948a4cb0d6812762a6c5736966c`.
- Append point: after line 393 (EOF). Anchor rows: R6 at `corpus/QUALITY.md:40`; R8 at :50;
  round-46 block heading :384; R50:390, R51:391, R52:392, R53:393.

## The block (R6 form; append after line 393)

```markdown
## Round-47 additions - R6 exception logs for anchor-moving landings and committed-instrument re-captures at next touch (append-only)

R6 form: every line above keeps its number; this block is appended after line 393 (the file is
88671 bytes before it, `head -c 88671 corpus/QUALITY.md | sha256sum` →
`95a09d5d375da260086181cc8207dc3341129948a4cb0d6812762a6c5736966c`; `wc -l` → 393 — draft-time
figures measured at lane tree `82a8bd7` with `corpus/QUALITY.md` clean against HEAD, placeholders
the L1 re-measures immediately before writing: a byte figure measured at draft time is a stale
premise under R19 if an earlier append in the same round moved it), and the round-46 block
(R50 line 390, R51 line 391, R52 line 392, R53 line 393) is not edited. Sources:
`corpus/lessons/round-47.md` § Mistakes (M47-1, M47-3), the line-number note recorded in
`corpus/instruments/r47-routed-defects.py:39-43`, `.ufo/waves/round-47/controls/capture-determinism.txt`.

| id | criterion | grounded in |
|---|---|---|
| R54 | A landing diff that moves bytes inside a file other lane files cite by line number — so R6's keep-every-line-at-its-number contract cannot hold — records the exception in the same round's lesson: the lesson names every `path:NN` anchor into the touched file whose cited line changed, and the arbiter is `anchorcheck.py` run over the citing files before and after the landing — the cites whose printed source lines change between the two runs are exactly the moved set, and a moved cite named nowhere is an unlogged exception, not a tolerated one (the D5 mine: landing the three fenced bullets into their real `## Search log`/`## Registry changes` sections and deleting the scaffold necessarily moves `corpus/SOURCES.md` line numbers below :90; the round-47 counter can only record the note in its docstring — `r47-routed-defects.py:39-43` — and no limb L1-L11 grades the log, so without this row the duty is advisory prose and the moved set lives nowhere a reader can find; M47-1). enforced-by: `python3 corpus/instruments/anchorcheck.py <file>` before/after (the r28 instrument; its r16 cadence already runs it after every edit to any cited lane file and at every round close); same-line corrections that keep their anchors (the F29 entry's unchanged 145-line count) stay inside R6's ordinary contract and are not exceptions. | `corpus/lessons/round-47.md:9` (M47-1, class `landing`, captured-by R48 — this row narrows the residual R48 does not cover: the anchor bookkeeping of the landing itself); `corpus/instruments/r47-routed-defects.py:39-43` (the recorded R6 exception note; `grep -n 'moved\|shift' corpus/instruments/r47-routed-defects.py` returns docstring lines only — no limb enforces it); `corpus/QUALITY.md:40` (R6, the contract this exception qualifies); `corpus/lessons/round-46-verifier-spotcheck.md` §8 D5 (via M47-1) |
| R55 | A pinned capture whose producing method is not a committed instrument — at the row's next touch (its recheck cadence), no committed command can produce a comparing re-capture of the pinned bytes — is re-captured with the committed instrument at that touch: the new capture is registered as a new row whose `teaches` opens `supersedes S### —` (rule 2), the old row's status change is logged old→new in the round's `## Registry changes` record, and the old capture is preserved as historical evidence, never deleted or re-pinned in place (the D7 mine: the admitted S074 row pinned a 42-line capture no committed instrument reproduces — the committed `capture-source.py --kind html` yields 610 lines for the same URL — so its 90d recheck could never produce the comparing re-capture its cadence promises; the repair re-captured the document as S076, sha-pinned in the round-47 manifest that `source-recheck.py` verifies exit 0 with thirteen located quotes, two same-instrument captures byte-identical (`controls/capture-determinism.txt`), S074 mined→rejected with used-by → the round-46 lesson, logged old→new; M47-3). R8 already requires the supersede row and the old→new log; R55 adds the trigger — a recheck that cannot reproduce, not only a corrected anchor or broadened scope; R49 already forces capture-method parity between admit and reject reads, not reproducibility of the pinned bytes. enforced-by: `python3 corpus/instruments/capture-source.py --id S### --url <row url> --kind html --out corpus/source-snapshots/<round>/S###.txt` then `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/<round>/manifest.json --source S###` (observed at tree `82a8bd7`: `S076:sha256 OK`, quotes Q1-Q12 `occurrences=1 anchor=568-600-ok`, exit 0); the absence of any committed producing command is itself the red state that fires the supersede. | `corpus/lessons/round-47.md:11` (M47-3, class `attribution`, captured-by R49 — this row narrows the residual R49 does not cover: capture reproducibility at the row's own recheck); `.ufo/waves/round-47/controls/capture-determinism.txt` (S075/S076 first=second digests, captured 2026-10-30T10:35:37Z/10:35:47Z, both HTTP 200); observed run receipt at tree `82a8bd7`: `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-47/manifest.json --source S076` → 13 `OK` lines + `S076:sha256 OK`, exit 0; `corpus/QUALITY.md:50` (R8) and :382 (R49), the rows this trigger extends; precedent supersede rows `corpus/SOURCES.md` S029/S030/S031/S060/S072 and the rule-2 note at :175 |
```

## Discrimination against the do-nothing controls

- **R54 vs R6-as-is (control = land D5 with no new row).** The landing is legal — R6's own
  exception is asserted nowhere as a criterion, and the round-47 counter merely *notes* it in
  its docstring (`r47-routed-defects.py:39-43`; grep `moved|shift` over the counter returns
  docstring lines 40-42 only, no limb L1-L11). Control outcome: anchors below `SOURCES.md:90`
  move; anchorcheck's before/after runs print changed source lines; nothing red fires; the
  moved set is recorded in no artifact a later reader or counter can query. R54 converts the
  advisory note into a named duty with a mechanical arbiter (the instrument R6 already names)
  without changing R6's ordinary contract.
- **R55 vs R8/R49-as-is (control = admit a capture with sha pin only).** The sha pin binds
  bytes (R48-style content binding) but nothing requires a committed producing command:
  S074 was admitted pinned, and its 90d recheck had no command that could produce a comparing
  re-capture — the exact spot-check §8 D7 finding (M47-3, `round-47.md:11`). R8 supplies the
  supersede mechanics and the old→new log; R49 supplies admit/reject method parity; neither
  fires on "no committed recipe". R55 names that trigger and the repair path; its enforce-by
  commands are committed instruments I exercised read-only (receipt above), so the row asks
  for nothing that does not exist.

## Verification performed (observed, not claimed)

- `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-47/manifest.json --source S076` at tree `82a8bd7` → `S076:sha256 OK`, `S076:Q1..Q12 OK occurrences=1 anchor=568-ok..600-ok`, exit 0 (matches claims.json C1 `plain` target line).
- `capture-determinism.txt` read: S075 and S076 `first=second` digests, 2026-10-30T10:35:37Z/47Z, both HTTP 200.
- Measurement commands above run at tree `82a8bd7`; QUALITY.md clean vs HEAD (porcelain empty).
- anchorcheck.py was NOT run against a landed tree (no landing exists in my scope): the R54
  enforce-by before/after form is verified only against the instrument's documented contract
  (`anchorcheck.py:1-12,72-77` — verifies backticked `path:NN` cites, prints the cited source
  lines, cadence "after every edit to any cited lane file"), not by an executed before/after
  pair. An unrun check has not passed; the L1 landing should run the pair.

## Limitations

- Byte figures and the append line 393 are draft-time values (R19); the L1 re-measures at
  landing — any earlier round-47 append to QUALITY.md invalidates them.
- R54's enforcement is partial by design: anchorcheck prints the moved-cite set mechanically,
  but "the lesson names them" stays a review duty (no counter limb grades the log this round;
  a future limb could grep the lesson for the anchor list).
- R55's trigger rides the row's existing recheck cadence: a row whose recheck never fires
  escapes the criterion until touched — the same exposure R8/R49 carry; it does not force a
  retroactive sweep of already-pinned rows.
- M47-1 and M47-3 already carry captured-by R48/R49; R54/R55 narrow residuals, they do not
  replace those rows. M47-6 (number-drift, `round-47.md:14`) is adjacent but distinct: it
  audits counts, not cite anchors — R54 cites it only through the D5 landing context.
- Both rows are drafts for the L1's integration; wave 2 attacks the integrated tree and
  wording may move there. M47-1/M47-3's own factual cells were taken as read from the frozen
  lesson, not re-derived beyond the receipts cited above.

## Bounds, tooling, scratch

- Writes: this file only (`w1/R47SrQual.md`). No `.draft/` dir — the deliverable is one block,
  embedded above. Scratch `/fast/scratch/hyaku/kasegi-r47/R47SrQual` was created, never used
  (no clones or work trees needed), and removed before yield.
- No git/jj mutation anywhere (read-only `rev-parse`/`status` only); no pacman invocation
  (host pause respected); no tools installed (none needed) — disk guard at pass start:
  `/fast/scratch/hyaku` 54% used, 375.0G free.
