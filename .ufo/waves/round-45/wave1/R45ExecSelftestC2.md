VERDICT: DRAFT-READY

Seat R45ExecSelftestC2 — counter selftest for C2 (`corpus/instruments/r45-c2-gate.py`, frozen; not edited).

Draft: `.ufo/waves/round-45/wave1/R45ExecSelftestC2.draft/r45-counters-selftest-c2.py` (stdlib, ~26 KB). Copy to `corpus/instruments/` is the L1's call.

## What it builds
A complete synthetic C2 tree per case under `$HYAKU_SCRATCH/kasegi-r45/R45ExecSelftestC2/c2st-*/tNNN/` (removed on exit; `--keep` skips removal):
- `corpus/README.md` frontier F01..F27, all `admitted`, F27 entry cell `` `knowledge/linux-kernel-security-bugs-process.md` ``.
- `corpus/SOURCES.md` census-valid, S071 row 11 cells, tier A, mined, opened 2026-10-28, snapshot sha256 in the anchor, used-by = the entry path.
- 64 knowledge files (entry + 63 stubs).
- Byte copies of `S071.txt`, `S072.txt`, `manifest.json` (round-45) and `source-recheck.py` (G4 runs it from the tree).
- Entry: provenance trio + five curly-quoted spans. Citations are LOCATED by search in the real S071.txt at build time (not hard-coded).

## Baseline (counter run on the unmutated tree; command: `r45-c2-gate.py --root <t001>`; printed)
```
gate G1 pass=1 read=rows=27 admitted=27 entry=corpus/knowledge/linux-kernel-security-bugs-process.md
gate G2 pass=1 read=source=1 verified-at=1 recheck=1
gate G3 pass=1 read=row-S071=ok
gate G4 pass=1 read=recheck-rc=0 quotes-ok=5 frozen-cores-missing=0
gate G5 pass=1 read=spans=5 located=5 failed=0 cores=4/4
gate G6 pass=1 read=knowledge=64
gate G7 pass=1 read=census-rc=0
c2-gate fixed=7/7 exit=0
```
Located citations (entry lines): 7-day ceiling `S071.txt:310-311`, AI-public `95-96`, binary-only `39-40`, unreproducible `41-43`, version `20-21`.

## Selftest run (re-run by me)
Command: `TMPDIR=<scratch> python3 r45-counters-selftest-c2.py`. Last line printed:
```
selftest cases=51 failures=0
```
51 = 3 controls (unmutated 7/7, no-op rewrite 7/7, 25-word genuine span 7/7 — the word-limit boundary) + 48 mutants. Each mutant asserts its targeted gate(s) printed `pass=0` and that all 7 gate lines were emitted. Every mutant was rejected, e.g.:
```
ok   mutant M01 fabricated 7-day quote: target=G5 failing=G5 fixed=6/7
ok   mutant M02 quote cited at wrong line (200): target=G5 failing=G5 fixed=6/7
ok   mutant M03 26-word quote: target=G5 failing=G5 fixed=6/7
ok   mutant M04 tier B: target=G3 failing=G3 fixed=6/7
ok   mutant M05 status queued: target=G3 failing=G3 fixed=6/7
ok   mutant M06 used-by missing (—): target=G3 failing=G3 fixed=6/7
ok   mutant M08 snapshot byte flipped: target=G3,G4 failing=G3,G4 fixed=5/7
ok   mutant M09 manifest Q5 removed: target=G4 failing=G4 fixed=6/7
ok   mutant M14 63 knowledge files: target=G6 failing=G6 fixed=6/7
ok   mutant M16 63 files + directory named *.md: target=G6 failing=G6 fixed=6/7
ok   mutant M17 duplicate F id (F25->F26): target=G1 failing=G1 fixed=6/7
ok   mutant M33 duplicate URL+scope row (E04): target=G7 failing=G7 fixed=6/7
ok   mutant M40 quote borrowed from S072 cited as S071: target=G5 failing=G5 fixed=6/7
```
Coverage: every gate G1–G7 has ≥3 independent mutants (G1: M17–M21; G2: M22–M25; G3: M04–M08, M26–M31; G4: M08–M13; G5: M01–M03, M36–M48; G6: M14–M16; G7: M32–M35). Requested set all present: fabricated quote (M01, M36–M39), quote at wrong line (M02, M46, M48), 26-word quote (M03), wrong tier (M04), status queued (M05), used-by missing (M06/M07), snapshot byte flipped (M08), manifest quote removed (M09), 63 files (M14), duplicate F id (M17).

Collateral failures (informational; targeted gate still 0): M21 F27 entry file missing also fails G2,G3,G5 (they all depend on entry_path); M29 10-cell row also fails G7 (census E01); M34 future `opened` fails G3 and G7.

## Do-nothing control (discrimination)
Command: `... r45-counters-selftest-c2.py --do-nothing-control` (stub counter printing seven `pass=1` lines + `fixed=7/7`). Printed:
```
selftest cases=51 failures=48
```
and `grep -c '^FAIL'` = 48: the selftest fails every one of the 48 mutants against a counter that rejects nothing, while the 3 controls still pass — so the 51/0 above is not a vacuous result.

## Mutants the counter FAILS to reject (weakness probes; informational, not counted as failures)
`probes accepted=5/7`. Exact tree recipes (apply to the baseline tree above); each printed `ACCEPTED (counter blind) failing=- fixed=7/7`:
- P1 whole-file citation range: change the 7-day span citation `` `S071.txt:310-311` `` to `` `S071.txt:1-372` ``. G5 locates any genuine quote in a window of the whole file; the line-pin is only as tight as the author's range. (A quote moved to a "wrong line" is only rejected when the range excludes the real line.)
- P2 used-by suffix: SOURCES.md S071 used-by `corpus/knowledge/linux-kernel-security-bugs-process.md.bak` (file created). G3 uses `p not in row[10]` (substring), census E11 only checks existence.
- P3 F27 sources cell says `S001` instead of `S071`. No gate reads the F27 sources cell.
- P4 manifest Q5: set S071 quote Q5 text to `Linux kernel developers take security very seriously.` (anchor 6) and add `"note": "with no version indication, your report will not be processed"` to the S071 record. source-recheck sees five valid quotes, and G4's frozen-core check is a text search of the whole manifest file, so the free-form note satisfies it.
- P5 same but the note placed on the S072 record: still accepted (the core text anywhere in the file counts).
Rejected probes: P6 (F27 entry cell lists a stub first → G2,G3,G5 fail), P7 (decoy `| F27 |` row inside a code fence → G1 fails, 28 rows).

## Limitations
- The synthetic tree copies the real snapshot, manifest and `source-recheck.py`; it exercises the counter's logic against the frozen captures, it does not re-validate the real round-45 tree (real F27/SOURCES/knowledge are not yet built here).
- G7 depends on `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` (counter default `SOURCES_CENSUS`); selftest inherits that dependency and today's date (opened 2026-10-28 must be ≤ census "today"; E08 passes on 2026-10-28).
- Counter's own `--root` only; I did not run mutants that need git (the counter never runs git).
- Targeted-gate assertion only; collateral gates are printed, not asserted exact.
- No tools installed; no git/jj mutation; lane tree untouched except this report and the draft directory. Scratch removed (`ls $HYAKU_SCRATCH/kasegi-r45/R45ExecSelftestC2` empty after run).
