# Round-94 controls proposed by the MutC1Counter seat (round 93)

Every item below is grounded in an executed probe; the receipt named in each row is in
`probes/` or `suites/` next to this file. Each control asserts a **limb line**, not only
an exit code: the round-93 `m3-labelled-file-scope` control records `rc=1` from a
traceback (see R1, `02-r1-shadow-repro.txt`), which an rc-only harness cannot tell
apart from a detected defect.

## PC-01 — `m3-line-count-delta` (kills M05; requires R1 fixed)
Fixture (`mkfixtures.py` F7): clone at the landing; append the label row
`SKILL.md:191  SKILL.md:191  CORRECT  No edit: ...`; append one line to `SKILL.md`;
commit. Run `--base-rev e15996bf... --after-rev <fixture> --map repair-map.tsv`.
Assert `rc=1` **and** `LIMB M3 FAIL same_files=True bad_lines=1`.
Observed: frozen counter → traceback, no LIMB line (`probes/P17-fx7-frozen.txt`);
R1-fixed counter → `LIMB M3 FAIL bad_lines=1` rc=1 (`P18`); R1-fixed+M05 → all limbs
pass rc=0 (`P19`).

## PC-02 — `m4-duplicate-basename` (kills M06)
Fixture (`mkfixtures.py` F2): the 437 cell edit with the frozen labels/map rows verbatim,
plus a tracked `notes/intake-surface.md` in the after tree (basename collision outside
`.ufo/`). Assert `LIMB M4 FAIL bad=triage-thresholds.md:437` and `rc=1`.
Observed: frozen rc=1 M4 FAIL (`P03`); M06 rc=0 (`P04`).

## PC-03 — `m5-anchor-hi-past-eof` (kills M08)
Fixture (`mkfixtures.py` F3): 454 repointed to `` `SKILL.md:827-9999` `` (SKILL.md has
1251 lines), label `SKILL.md:827-9999`, matching map row. Assert
`LIMB M5 FAIL out_of_range=triage-thresholds.md:454`.
Observed: frozen rc=1 (`P05`); M08 rc=0 (`P06`).

## PC-04 — `m5-anchor-last-line-plus-one` (kills M09)
Fixture (`mkfixtures.py` F4): 454 repointed to `` `SKILL.md:1252` `` — the empty element
`split("\n")` sees after the trailing newline of a 1251-line file. Assert
`LIMB M5 FAIL out_of_range=triage-thresholds.md:454`.
Observed: frozen rc=1 (`P07`); M09 rc=0 (`P08`).

## PC-05 — `m6-pin-truncated` (kills M14)
No fixture: run the landing with `--map-sha256` set to the first 16 hex of
`7ab66a7fc8a90cf9...` followed by 48 zeros. Assert `LIMB M6 FAIL` and `rc=1`.
Observed: frozen rc=1 (`P20`); M14 rc=0 (`P21`).

## PC-06 — `excluded-pair-unmapped` (kills M12)
Counter with a real `EXCLUDED` entry (round 92 carried two; round 93 carries none).
Fixture (`mkfx8.py`): labels name the edits at 454 and 58, only 454 is mapped, the 58
pair is the excluded one. Assert `rc=0` and `kinds=excluded=1,range=1`.
Observed: `excl-base` rc=0 (`P23`); the same data with M12 rc=1,
`unapplied=triage-thresholds.md:58/SKILL.md:117` (`P24`); frozen counter (EXCLUDED empty)
rc=1 (`P22`) — showing why the defect is invisible this round.

## PC-07 — `excluded-pair-absent-from-labels` (kills M13)
Counter with `EXCLUDED = {(site, key)}` for a pair that is **not** in the labels file.
Assert `LIMB M10 FAIL` (the `set(EXCLUDED) <= set(kinds)` conjunct) and `rc=1`.
Observed: `excl-base-absent` rc=1 (`P15`); with M13 rc=0 (`P16`).

## PC-08 — `content-repair-drop-token` (kills M17; restores round-92 kind coverage)
Fixture (`mkfixtures.py` F5): 454 labelled `content-repair` with
`Replace with — (drop only the `SKILL.md:494-506` token)`, the token removed from the
line, map `new` empty. Assert `rc=0` and `kinds=drop-token=1`.
Observed: frozen rc=0 (`P09`); M17 rc=1 with `kinds=unknown=1` and `M9 unbound` (`P10`).

## PC-09 — fix R1 and assert on stdout (control-harness defect)
`art/knowledge-meter.py:282` rebinds the argparse namespace:
`b, a = file_at(B["tree"], rel), file_at(A["tree"], rel)`, so `a.map_sha256`
(line 399) raises `AttributeError: 'str' object has no attribute 'map_sha256'` whenever
the M3 labelled-file union adds a file. The crash precedes the LIMB print loop: the
counter prints no `LIMB`/`KNOWLEDGE-METER-RESULT` line and exits 1.
Consequences:
* the frozen `m3-labelled-file-scope` control passes on the traceback (rc-only check),
  so round 93 has **no** working test of the new non-knowledge walk;
* the claim sentence "M3 walks every labelled file" is inoperative.
Fix (`variants/r1fix.py`): rename `a` to `a_txt` in both lines. Then have
`c1-controls-r93.py` require a matching `LIMB <name> FAIL` (or `KNOWLEDGE-METER-RESULT
fail`) line in addition to the expected rc.
Observed: traceback (`02-r1-shadow-repro.txt`, `P17`); fixed counter prints
`LIMB M3 FAIL bad_lines=1` (`P18`).

## PC-10 — bind lane-root tokens inside a cell replacement (R2), or narrow the wording
`expected_edit`/M4 capture lane-root values only when the whole `new` field is
`` `SKILL.md:N[-M]` `` (`LANEVAL` is `^...$`). A cell-repair replacement is prose, so the
lane-root token it carries is never bound or range-checked. Probe F1 changes 437's
`SKILL.md:176-178` to `SKILL.md:9999-10000` (past EOF): the frozen counter still prints
`LIMB M5 pass out_of_range=none` and rc=0 (`P01`). Either scan `new` for
`SKILL.md:\d+(-\d+)?` occurrences when the row is a cell repair and range-check each, or
narrow the M5 wording from "every written value" to "the row's primary value".
Not a claim re-score: on the landing the token is `SKILL.md:176-178`, inside the
1251-line file, so every limb that examines it passes either way.

## Not proposed (equivalent mutants)
* M07 — for a bare lane-root value `classify()` is `INTERNAL` iff `SKILL.md` exists,
  which the `"SKILL.md" not in A["tracked"]` guard and M5's `file_at(...) is None` check
  already require.
* M10 — `unknown` kinds are not in the `("excluded", "no-edit")` filter, so an unknown
  pair always lands in `want` and is caught by `unapplied`; `not unknown` is redundant.
* M11 — a mapped pair outside `want` always fails M9 (no label row, `no-edit`/`unknown`
  give `exp is None`, and an `EXCLUDED` pair is rejected by the same condition), so
  `unlabelled` cannot change the verdict.
