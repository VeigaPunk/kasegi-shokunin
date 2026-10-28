VERDICT: DRAFT-READY

Seat R45W2ExecSelftestC2 — selftest for C2 counter v1.1 (`corpus/instruments/r45-c2-gate.py`, not edited), attacked on an export of lane commit 6662a4276b6f7bd61e23e12058414e09dd71b9e4 (`git archive … | tar -x -C $HYAKU_SCRATCH/kasegi-r45/selftest-c2/export`).

Draft: `.ufo/waves/round-45/wave2/R45W2ExecSelftestC2.draft/r45-counters-selftest-c2.py` (stdlib, 46486 bytes, sha256 bb3197a8ef7ba0ad2de7682b55d2664cb233c4e7ca7b356cfca0ef1aab739335). Usage: `python3 r45-counters-selftest-c2.py [--lane DIR] [--counter PATH] [--do-nothing-control] [--keep]`; `--lane` takes the tree whose counter and round-45 captures are used (I passed the export). Last printed line `selftest cases=<N> failures=<F>`; exit 0 iff F==0. Scratch: `$HYAKU_SCRATCH/kasegi-r45/selftest-c2/c2st-*` (removed on exit; the whole `selftest-c2` dir removed by me at the end).

## Finding 1 — the v1.1 counter rejects every mutant (command and printed output)
Command: `HYAKU_SCRATCH=/fast/scratch/hyaku python3 <draft> --lane <export>` → rc=0, last line printed:
```
selftest cases=115 failures=0
```
115 = 12 controls + 103 mutants (`grep -c '^ok   mutant'` = 103). Probes (14) are printed, never counted. Every mutant printed `pass=0` on its targeted gate(s) with all seven gate lines present; no mutant survived.

Control line set that passed 7/7 (these prove the mutants fail for the targeted reason, not because the tree is broken): C0 unmutated synthetic tree; C1 no-op README rewrite; C2 25-word genuine span; C3 entry exactly 3000 bytes; C4 table of exactly 6 data rows; C5 decoy F27 row inside a fence is ignored; C6 decoy F27 row inside an HTML comment is ignored; C8 grader env `SOURCES_CENSUS=/nonexistent/…` is ignored; C9 tree-local `source-recheck.py` (`raise SystemExit(1)`) is ignored; C10 own-lane copy of the real source-recheck passes; C11 the real export tree itself with real pins (no override) → 7/7; C12 non-`.md` file in `knowledge/` not counted.

## Finding 2 — coverage of the nine required v1.1 gates (all rejected)
Quoted result lines (re-run output):
- uncited curly span: `ok mutant N01 uncited curly span (new sentence): target=G5 failing=G5 fixed=6/7`; also N02 (uncited restatement of a REAL quote), N03 (citation separated by words), N04 (em-dash + unparenthesised citation), N05 (uncited span in a table cell) — all `failing=G5`.
- comment-hidden F27 row: `N06 … target=G1 failing=G1,G2,G3,G5,G6 fixed=2/7`; inline-comment variant N07 identical.
- fenced S071 row: `N10 fenced S071 row: target=G3 failing=G3 fixed=6/7`; also N11 (HTML-comment S071 row `failing=G3`), N12 (row moved under `## Paths`: `failing=G3,G7`), N57 (decoy S071 row in a comment: the counter's G3 ignores it, census E-code trips G7 → `failing=G7`).
- entry shared with another F row: `N13 F27 entry shared with the F26 row: target=G1 failing=G1,G2,G3,G5,G6 fixed=2/7`.
- symlinked entry: `N16 F27 entry is a symlink (to a file outside knowledge/): target=G1 failing=G1,G2,G3,G5,G6 fixed=2/7`; N17 directory entry same.
- missing section: N21–N24 (each of the four headings removed) `target=G2 failing=G2 fixed=6/7`; N25 suffixed heading and N26 one-space-indented heading `failing=G2`.
- short entry: `N29 short entry: 2999 bytes: target=G6 failing=G6 fixed=6/7` against control `C3 entry exactly 3000 bytes … fixed=7/7`; N30 2500 bytes.
- dangling xref: N31 (`:9999`), N32 (`:0`), N33 (ghost file), N34/N35 (one required target replaced), N36 (none), N37/N38 (target truncated below the cited line), N39 (target is a directory) — all `target=G2 failing=G2 fixed=6/7`.
- padded knowledge dir: `N40 … base name swapped for a pad name (still 64): target=G6 failing=G6`; N41 base renamed (still 64) `failing=G6`; N42 pad added + cross-referenced base dropped (64) `failing=G2,G6`; M14 65 files `failing=G6`; M13 63 files `failing=G6`.
- other v1.1 gates covered: N18/N19/N20 (unrelated existing stub / empty / header-only entry), N27/N28 (5-row table / none), N14/N15 (two or no knowledge paths in the F27 cell), N09 (live decoy F27 row), N43 (self-pinned empty snapshot: `failing=G3,G4,G5`), N44/N45 (one trailing newline appended to snapshot/manifest: pins are byte-exact), N46 (Q5 core moved to a manifest note), N47 (tree-supplied always-OK `source-recheck.py` + flipped snapshot: `failing=G3,G4`), N48/N49 (own-lane source-recheck silent / exits 1 after OK lines: `failing=G4`), N50–N53 (source line tail / URL suffix / trio below line 8 / recheck line without `--source S071`), N54 (grader env `SOURCES_CENSUS=<always-ok script>` + kind enum violation → `failing=G7`), N55 (REAL pins active against the synthetic stub names → `failing=G6` only), N56 (real export tree + `R45_PINS_OVERRIDE` with a wrong S071.txt hash → `failing=G3`, proving the override seam works).
- wave-1 mutants kept (M01–M46, the ones that still apply): fabricated/near-miss/borrowed quotes, wrong/reversed/cut citations, 26-word span, tier/status/used-by/anchor/URL/opened/kind/duplicate/future/dangling row defects, manifest edits, 63/65 knowledge files, duplicate id, queued rows, 26 rows, entry missing, trio defects. Wave-1 mutants dropped: M13 (tree `source-recheck.py` absent — the tree no longer carries one, v1.1 uses its own lane; replaced by N47–N49/C9/C10) and M16 (directory named `*.md` — moved to probe P4, see Finding 4); wave-1 probes P4/P5 (manifest note) became mutant N46, P6 (two paths in F27 cell) became N14, P7 (fenced decoy F27) became control C5.

## Finding 3 — discrimination against a do-nothing control and against weakened counters
- `--do-nothing-control` (stub counter printing seven `pass=1` + `fixed=7/7`), printed last line: `selftest cases=115 failures=103`; `grep -c '^FAIL'`=103, `grep -c '^ok   control'`=12. All 103 mutants fail, the 12 controls still pass.
- Weakened-counter check (stronger than do-nothing): I copied the export to scratch, applied one single-line weakening to its `r45-c2-gate.py` per run, and ran the selftest against it (`--lane` = the copy). Each weakening was detected (failures>0) by the named cases:
```
uncited check removed: failures=5 (N01 N02 N03 …)           base-names pin ignored: failures=4 (N40 N41 N42 …)
symlink check removed: failures=1 (N16)                      shared-row check removed: failures=1 (N13)
manifest pin ignored: failures=2 (N45 N46)                   snapshot pin ignored: failures=2 (N43 N56)
xref existence ignored: failures=9 (N31 N32 N33 …)           table floor lowered: failures=1 (N27)
entry size floor removed: failures=4 (N19 N20 N29 …)         sections ignored: failures=6 (N21 N22 N23 …)
comment stripping removed: failures=3 (C6 N06 N11)           fence handling removed: failures=3 (C5 N08 N10)
registry-only restriction removed: failures=1 (N12)          census env honored: failures=2 (C8 N54)
tool root = tree root: failures=12 (C0 C1 C2 …)              25-word limit removed: failures=1 (M03)
```
16/16 weakened counters caught; no weakening survived. (The weakened copies are scratch only; not retained.)

## Finding 4 — probes: what v1.1 accepts (informational; none counted; each printed `ACCEPTED (counter blind) failing=- fixed=7/7`)
Attack target: `r45-c2-gate.py` v1.1 on the export, using the same synthetic tree. Accepted:
1. P1 whole-file citation range `S071.txt:1-N` on a true quote (G5 window is the cited range; any real quote locates).
2. P2 `used-by` = entry path + `.bak` (G3 `p not in row[10]` is a substring test).
3. P3 F27 row's `sources` cell says S001 not S071 (G1 never reads cell 5).
4. P4 a base knowledge file replaced by a DIRECTORY named `stub-61.md` (G6 `os.listdir` + `.endswith('.md')` counts directories, as `find -name '*.md'` also does; names intact).
5. P5 a base knowledge file emptied (G6 pins only the 63 NAMES, not contents).
6. P6 xref cited line valid but unrelated (`:20`; G2 checks only that the line number is in range — not what it says).
8. P8/P9 a fabricated quote in single curly marks `‘…’` or straight marks `"…"`, uncited (G5 only scans double curly marks).
9. P10 a stray unbalanced opening `“` (no closing mark ⇒ no span matches).
10. P12 a table of six junk 3-column rows `| a | b | c |` with the cited spans moved to bullets (G2's `table-rows` counts any 3-column rows).
11. P13 a span citation followed by an extra `S072.txt:1` citation; P14 a junk HTML comment after a citation.
Rejected probes: P7 (required heading only inside an HTML comment → `failing=G2`), P11 (uncited curly span inside an HTML comment → `failing=G5`; the counter scans the raw entry body).
Result for the brief's "any mutant the v1.1 counter fails to reject": none among the 103 counted mutants; the 12 accepted probes above are the residual blind spots.

## Limitations
- G7 depends on the host file `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` and today's date (opened 2026-10-28 must be ≤ census "today"); the selftest inherits that dependency and the real tree C11 depends on the real lane SOURCES/knowledge at the export commit.
- Controls C0–C12 and 12 of the mutant targets depend on the pinned captures being the same bytes in `--lane` as in the counter's pins (true for the export; the selftest computes S071/manifest pins from `--lane` for the synthetic override, so a drifted lane capture would not be flagged by the override cases — only by C11/N55).
- Synthetic base names are 61 `stub-NN.md` plus the two cross-referenced names; the selftest never exercises the real 63-name hash except via C11/N55.
- The weakened-counter check (Finding 3) was a one-shot script in scratch (not part of the draft) and covers 16 single-line weakenings, not all gates' internals.
- Not tested: concurrent runs, non-UTF-8 entries, entry >1 MB, symlinked `corpus/knowledge` directory, case-insensitive filesystems.
- No tools installed; no pacman; no git mutation; export and scratch only. Draft not copied into `corpus/instruments/` (L1's call). Selftest wall time ≈ 13 s.
