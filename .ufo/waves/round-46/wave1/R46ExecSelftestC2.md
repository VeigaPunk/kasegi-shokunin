VERDICT: DRAFT-READY

Seat R46ExecSelftestC2 (executor, round 46, C2 counter selftest). Draft only; the counter was not edited (`sha256sum corpus/instruments/r46-c2-gate.py` -> `0ee958578b5923706178081a94dae471682f02f74492bb4a3b54a118c12ec3f6`, no `M` for it in `git status --short`). No tools installed. No git mutation.

## Deliverable
`/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-46/wave1/R46ExecSelftestC2.draft/r46-counters-selftest-c2.py` (stdlib, 37751 bytes, `py_compile` clean). L1 lands it as `corpus/instruments/r46-counters-selftest-c2.py`.

Usage: `python3 r46-counters-selftest-c2.py [--lane DIR] [--pure DIR] [--counter PATH] [--do-nothing-control] [--keep] [-v]`; defaults: lane = `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, pure = `/fast/scratch/hyaku/kasegi-r46/L1/pure`. Scratch: `$HYAKU_SCRATCH/kasegi-r46/R46ExecSelftestC2/c2st-*` with explicit TMPDIR, removed in `finally`; pure and lane are only read.

What each case tree is (built from a `shutil.copytree` of the pure export, so the counter's REAL pins hold; `R46_PINS_OVERRIDE` is never set):
- README: pure frontier F01..F27 plus a live `| F28 | ... | admitted | `corpus/knowledge/github-private-vulnerability-reporting.md` | S073 | ... |` row inserted after F27.
- SOURCES: S073 row (11 cells, tier A, `mined`, opened 2026-10-28, canonical URL in source cell, `sha256 66c96a61...df1930` in anchor, `180d`, used-by = entry) inserted after the last S0nn row.
- Entry (3600 bytes): `source: S073 — <URL> — ...`, `verified-at: 2026-10-28`, `recheck: cd <lane> && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-46/manifest.json --source S073 # 180d`, the four sections, an 8-row 3-cell table, seven curly spans each followed by (`S073.txt:N`) where N comes from a window search of the real capture (never hard-coded), covering all five frozen cores, `corpus/knowledge/linux-kernel-security-bugs-reporting-process.md:11-12` and `corpus/knowledge/ai-assisted-finding-validation.md:7-8,15`.
- `corpus/source-snapshots/round-46/{S073.txt,manifest.json}` byte copies from the lane.

## Findings (every number below is from a re-run I performed)

### F1. Complete tree reaches 7/7; null tree does not
Command: `cd <scratch> && python3 .../r46-counters-selftest-c2.py -v`. Printed:
```
ok   null    null-pure-base-unmodified fixed=1/7 failing=['G1', 'G2', 'G3', 'G4', 'G5', 'G6']
       gate G1 pass=0 read=rows=27 admitted=27 dup=0
       gate G2 pass=0 read=F28-rows=0
       gate G3 pass=0 read=row-S073=absent-or-malformed
       gate G4 pass=0 read=manifest-absent
       gate G5 pass=0 read=F28-rows=0
       gate G6 pass=0 read=knowledge=64 base-names-intact=1 entry-bytes-ok=0
       gate G7 pass=1 read=census-rc=0 ok-line=1
ok   control ctl-complete-tree fixed=7/7 failing=[]
```
The same null read was obtained by running the counter directly on the pure export: `c2-gate fixed=1/7 exit=1`.
Complete-tree counter lines inside the harness (from the mutant dumps, where the untouched gates keep their reads): `gate G1 pass=1 read=rows=28 admitted=28 entry=corpus/knowledge/github-private-vulnerability-reporting.md`, `gate G2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 table-rows=8 xrefs=2/2`, `gate G3 pass=1 read=row-S073=ok`, `gate G4 pass=1 read=recheck-rc=0 quotes-ok=8 frozen-cores-missing=0`, `gate G5 pass=1 read=spans=7 located=7 failed=0 uncited=0 cores=5/5`, `gate G6 pass=1 read=knowledge=65 base-names-intact=1 entry-bytes-ok=1`, `gate G7 pass=1 read=census-rc=0 ok-line=1`. The harness asserts `fixed=7/7 exit=0` on the line `c2-gate fixed=7/7 exit=0` for ctl-complete-tree.

### F2. Final result
```
selftest cases=95 failures=0
```
95 = 1 null + 11 controls + 83 mutants (10 further probes are printed, not counted). Wall time about 18-20 s. The counter rejected EVERY mutant: no counter hole found among the 83 recipes, including the 12 card-named ones:
| card mutant | case | targeted gate read |
|---|---|---|
| fabricated quote | mut-fabricated-quote | `gate G5 pass=0 read=spans=7 located=6 failed=1 uncited=0 cores=4/5` |
| quote at wrong line | mut-quote-at-wrong-line (cite 577 -> 200) | `gate G5 pass=0 read=spans=7 located=6 failed=1 uncited=0 cores=4/5` |
| 26-word quote | mut-26-word-quote (real words of S073.txt line 566) | `gate G5 pass=0 read=spans=8 located=7 failed=1 uncited=0 cores=5/5` |
| wrong tier | mut-wrong-tier-B | `gate G3 pass=0 read=bad=tier` |
| status queued | mut-status-queued | `gate G3 pass=0 read=bad=status` |
| used-by missing | mut-used-by-missing-dash | `gate G3 pass=0 read=bad=used-by` |
| snapshot byte flipped | mut-snapshot-byte-flipped-nonquote | `gate G3 pass=0 read=snapshot-not-the-pinned-capture` and `gate G4 pass=0 read=recheck-rc=1 quotes-ok=0 frozen-cores-missing=0` (5/7); in-quote-line flip also fails G5 |
| manifest quote removed | mut-manifest-quote-removed-Q8 | `gate G4 pass=0 read=manifest-not-the-pinned-bytes` (Q6 removal likewise) |
| 64 files | mut-64-files-one-base-deleted | `gate G6 pass=0 read=knowledge=64 base-names-intact=0 entry-bytes-ok=1` |
| duplicate F id | mut-duplicate-f-id (F26 id -> F27) | `gate G1 pass=0 read=rows=28 admitted=28 dup=1` |
| F28 row in HTML comment | mut-f28-row-in-html-comment-block | `gate G1 pass=0 read=rows=27 admitted=27 dup=0` (G2,G3,G5,G6 also fail as collateral: entry path unresolved) |
| trio only in fenced block | mut-entry-trio-only-in-fenced-block | `gate G2 pass=0 read=source=0 verified-at=0 recheck=0 sections=4/4 table-rows=8 xrefs=2/2` |

Other mutant families (all rejected, each asserting its target gate pass=0 and that no gate outside target + stated collateral failed): G5 (core inside a 33-word span, uncited curly quote, core span replaced by prose for `ai` and for `enabled` and for `merge`, fabricated quote inside a fenced block, reworded quote, one-line-short citation window); G3 (anchor sha wrong/missing, opened 2026-10-27, source cell without canonical URL, 10-cell row, row in comment, row after `## Paths`, duplicated row, absent row, used-by = other existing file); G3+G4(+G5) (snapshot trailing newline, absent, self-pinned empty file with its own sha in the anchor, planted always-OK tree `source-recheck.py` plus a flipped byte); G4 (manifest quote text edited, sha zeroed, trailing newline, absent); G6 (66 files, base file swapped for a pad file, base file renamed, base file one byte longer, entry 2999 bytes, entry deleted while row kept); G1 (27 rows, F29 extra row, duplicate F28 row, F28 in inline comment / backtick fence / tilde fence, status `queued`, status only in fourth cell, entry file missing, entry shared with F27, two paths in entry cell, no path, entry is a symlink); G2 (trio in HTML comment, trio below line 8, wrong URL, wrong source id, wrong date, recheck absent / `--source S071` / not source-recheck.py, each of the four section headings renamed, 5 data rows, 4-cell rows, each of the two xrefs missing, xref line 999, line 0, xref to a missing file); G7 (extra dangling used-by, bad kind, invalid ISO recheck `2026-13-45`, opened 2099-01-01, SOURCES.md absent).

### F3. Controls (11) all print 7/7
ctl-complete-tree, ctl-25-word-span-boundary, ctl-range-citation-577-578, ctl-entry-exactly-3000-bytes, ctl-six-table-rows-boundary, ctl-whitespace-and-markup-in-span, ctl-f28-decoy-in-comment-and-fence, ctl-s073-decoy-in-comment-after-live-row, ctl-trio-first-lines-plus-extra-fenced-block, ctl-unrelated-env-vars-ignored, ctl-tree-supplied-planted-recheck-ignored: each printed `fixed=7/7 failing=[]`. Boundaries therefore hold on both sides (25 words pass, 26 fail; 3000 bytes pass, 2999 fail; 6 table rows pass, 5 fail).

### F4. Do-nothing control
Command: `python3 r46-counters-selftest-c2.py --do-nothing-control` (stub counter prints seven `pass=1` lines and `c2-gate fixed=7/7 exit=0`). Printed last line `selftest cases=95 failures=84`, rc=1: all 83 mutants plus the null-tree case are reported as accepted; the 11 controls stay `ok` (as they must). So the selftest discriminates: the 0-failure run above is not vacuous.

### F5. Harness defects found and fixed during my own re-runs (not counter defects)
First full run printed `selftest cases=95 failures=3`: (a) mut-opened-wrong-date hit the S071 row because the replace pattern was not unique (fixed by pinning on the S073 used-by cell); (b) mut-f28-entry-shared-with-f27 appended text after the closing pipe of the F27 row, outside any cell (fixed: edit the entry cell); (c) mut-census-bad-recheck used `someday`, which `sources-census.sh:582` accepts as a symbolic cadence (`function symbolic(s) { return s ~ /^[A-Za-z][A-Za-z0-9 _-]*$/ }`); replaced by the invalid date `2026-13-45`. After the fixes: `selftest cases=95 failures=0`.

### F6. Probes (printed, not counted): behaviours the counter accepts, each a 7/7 read
Recipes are in the script; all printed `fixed=7/7 failing=[] (ACCEPTED)`:
1. probe-wide-window-citation-1-589-for-real-quote: cite `S073.txt:1-589` for a real quote that lives at 577 -> accepted (the window is any N..M, no width cap).
2. probe-core-quote-from-page-chrome-line: a located curly quote from navigation chrome (`Collaborate in a fork`) -> accepted.
3. probe-single-curly-quotes-uncited: ‘single’ curly quotes are never read as spans.
4. probe-straight-quoted-fabrication: `"GitHub guarantees a response within 24 hours"` in straight quotes -> invisible to G5.
5. probe-fabricated-prose-no-quote-marks: unquoted false claim -> invisible to G5.
6. probe-extra-knowledge-subdir-file: `corpus/knowledge/sub/extra.md` is not counted (maxdepth 1).
7. probe-junk-table-rows-with-quotes-in-bullets: six `| a | b | c |` rows satisfy `table-rows>=6` (G2 counts any 3-cell pipe line). Same class as r45's junk-table case; the v1.2 docstring says "real tables only" but the limb only counts 3-cell lines.
8. probe-unclosed-html-comment-before-f28-row: `<!--` with no `-->` before the F28 row: the counter keeps the row live though a renderer would hide it.
9. probe-four-tick-fence-with-inner-three-tick-line: a 4-backtick fence containing a 3-backtick line closes early in `live_lines`, so a row a renderer shows as code is counted live.
10. probe-entry-pad-is-garbage-bytes: a 9000-byte entry of padding passes G6's 3000-byte floor.
These are design limits for the non-author closure to re-open by hand, not misses of the card-named recipes. Dead code noted in the counter: `if len(raw) != 1 or (False):` in `g1` (the `(False)` arm is unreachable); the variable names `f27` in `entry_path`/`g1` hold the F28 rows (harmless).

## Limitations
- Mutants run against the pinned real base (pure at base 914ca0b); a different base knowledge set fails G6 by design.
- Each mutant is a single recipe on one synthetic tree; "rejects the recipe" is not "rejects every variant". Collateral gate sets were predicted before running and then confirmed; they are enforced (an unexpected extra failing gate counts as a failure).
- G4 and G7 run the lane's `source-recheck.py` and the fleet `scripts/sources-census.sh` as they are on this host; the selftest does not mutate those.
- The synthetic entry's prose is test scaffolding, not the real F28 entry; its xref line numbers (`:11-12`, `:7-8,15`) are in-range but not semantically audited.
- No live target contacted; documentation only. No credential material used.
- Verification actually performed by me: the selftest end-to-end over all 95 cases (once with failures=3 before the harness fixes, then failures=0 on four later runs including one -v run), once under `--do-nothing-control`, `py_compile`, and the raw counter on the pure export. Scratch dirs removed (`ls /fast/scratch/hyaku/kasegi-r46 | grep -c C2-run` -> `0`; seat dir removed by the script's finally block).

Main should run after landing: `python3 corpus/instruments/r46-counters-selftest-c2.py` (expect `selftest cases=95 failures=0`) and, with `--do-nothing-control`, expect `failures=84`.
