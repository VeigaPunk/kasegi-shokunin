VERDICT: BROKEN

Scope of the verdict: the invariant attacked is "the committed selftest
`corpus/instruments/r46-counters-selftest-c2.py` pins the behaviour of the committed
counter `corpus/instruments/r46-c2-gate.py`". Against my own 41-mutant independent
battery (all edits outside the frozen `C2_MUTANTS` table in `corpus/instruments/r46-mutbat.py`)
the selftest stays silently green on 22 of 41 mutants; 17 of those survivors carry a
concrete witness tree on which the mutated counter's verdict differs from the pristine
counter's. This is a coverage finding for the C1 selftest-extension work, not a change
to any contract: the counter, the selftest, the battery and the frozen claims file were
touched nowhere (sha256 before/after identical), and the frozen battery before-value
reproduced (`baseline selftest cases=137 failures=0 exit=0`).

# What was built

- `mutants.py` — 41 single-edit mutants of `r46-c2-gate.py`, each verified to occur
  exactly once and verified disjoint from the frozen battery table (all 41
  `count=1`, none `[IN FROZEN BATTERY]`).
- `run.py` — mutbat-equivalent grading: each mutant is applied to a scratch copy of
  `corpus/instruments/`, the committed selftest is run with `--counter <mutant copy>
  --pure <pure2 copy>`; `failures>0` = caught, `failures==0` = survivor.
- `witness_runner.py` + `witnesses.py` — for every survivor, a concrete tree (built by
  the committed selftest's own builder) on which pristine and mutated counters are run
  side by side; a survivor with a differing gate vector is a genuine hole, a survivor
  with identical vectors on every constructed input is argued equivalent.
- Do-nothing control: the committed selftest's own `--do-nothing-control` mode
  (stub counter always printing 7/7) — run and reported below.

# Findings (each: mutant -> command -> printed output)

F1. Baseline (pristine detector is clean; without this every verdict is inconclusive).
    Command: `python3 r46-counters-selftest-c2.py --pure /fast/scratch/hyaku/kasegi-r46/R46bMutSelfC2b/pure`
    Output (tail): `selftest cases=137 failures=0` (exit 0). Reproduced three times
    (baseline pass of each sweep).

F2. Do-nothing control (the detector is not vacuous).
    Command: `python3 r46-counters-selftest-c2.py --pure <pure> --do-nothing-control`
    Output (verbatim tail, `R46bMutSelfC2b.draft/dnc-control.log`):

    ```
    probe       probe-entry-pad-is-garbage-bytes fixed=7/7 failing=[] (ACCEPTED) -- G6 floor is bytes, not content
    selftest cases=137 failures=118
    ```

    The stub counter that always prints `c2-gate fixed=7/7 exit=0` makes 118 of the 137
    cases report `FAIL ... <- ACCEPTED-targeted-gate-passes=[...]` (the remaining cases
    are the null/probe classes that do not assert a rejection). The grading loop
    therefore discriminates: a counter that cannot fail cannot be reported as caught.

F3. Sweep result. Command: `JOBS=8 python3 run.py` (two passes; second pass resumed the
    first after my own wall-clock timeout). Output (verbatim tail):

    ```
    counter-sha256-after=647bd5b7b62685519d8d396bf2d02eca7ad0bb440dd5c4041beabfaa45ea2909 restored=True
    SUMMARY mutants=41 caught=19 survivor=22 drift=0 baseline_failures=0 counter_restored=True
    ```

    Counter restored: `647bd5b7b62685519d8d396bf2d02eca7ad0bb440dd5c4041beabfaa45ea2909`
    before and after (the lane file was never opened for writing; mutants live only in
    `$HYAKU_SCRATCH/kasegi-r46/R46bMutSelfC2b/work/`).

F4. The 19 caught mutants (each graded `caught` by the committed selftest; first-fail
    line quoted from `run.log`/`run2.log`):
    X02-G1-dup-ignored (`mut-duplicate-f-id ... <- ACCEPTED-targeted-gate-passes=['G1']`),
    X05-G2-table-floor-5 (`mut-table-five-data-rows`, 4 failures), X09-G2-xref-lower-bound-dropped
    (`mut-xref-line-zero`), X11-G2-source-url-clause-dropped (`mut-source-line-wrong-url`),
    X12-G2-xref-refok-lenient (`mut-xref-line-out-of-range`, 2 failures),
    X15-G3-url-substring (`mut-row-url-wrapped-in-other-host`), X16-G3-tier-allows-B
    (`mut-wrong-tier-B`), X17-G3-opened-any-date (`mut-opened-wrong-date`),
    X18-G3-scope-words-5 (`mut-row-scope-seven-words`), X19-G3-recheck-cell-soon
    (`mut-row-recheck-cell-filler`), X21-G3-teaches-words-5 (`mut-row-teaches-seven-words`),
    X23-G4-anchor-count-5 (`mut-manifest-six-distinct-anchors-repinned`),
    X27-G5-span-12-lines (`mut-citation-13-lines`), X28-G5-words-26 (`mut-26-word-quote`),
    X29-G5-uncited-1 (`mut-uncited-curly-quote`, 2 failures), X31-G5-cores-count-lenient
    (`mut-citation-without-quote-marks-for-core`, 5 failures), X32-G5-live-spans-from-raw
    (`mut-core-row-in-html-comment`, 2 failures), X37-G6-content-exempt-pinned-too
    (113 failures — degenerate: it re-pins the two C1 entries and breaks every control),
    X39-G7-census-reads-lane-file (`mut-census-dangling-extra-used-by`, 5 failures).

F5. The 17 genuine coverage holes — survivor + witness where the gate vectors differ.
    For each: mutant, witness input, and the two printed gate lines (`pristine=…/7`,
    `mutant=…/7`, gate vector `G1..G7`). Full per-gate output is in
    `R46bMutSelfC2b.draft/witness-results.json`; the vectors quoted here are from
    `witness_runner.py` stdout.

    1. X01-G1-src-id-wildcard (`\bS073\b` -> `\bS07\d\b` in the F28 row's sources cell).
       Witness: F28 row cites S071. `pristine=6/7 0111111 | mutant=7/7 1111111`
       (pristine: `gate G1 pass=0 read=F28-sources-cell-lacks-S073`).
       Missing case class: a frontier row whose sources cell names a *different* S-id.
    2. X03-G1-admitted-prefix (`== "admitted"` -> `.startswith("admitted")`).
       Witness: F27 status cell `admitted (pending)`. `pristine=6/7 0111111 | mutant=7/7 1111111`
       (pristine: `gate G1 pass=0 read=rows=28 admitted=27 dup=0`).
       Missing case: a non-F28 row whose status cell is admitted-but-not-exactly.
    3. X04-G2-package-floor-6 (Falsifiable-section floor 12 -> 6).
       Witness: package rule cut to 7 words ("Check each step against `S073.txt:564`.").
       `pristine=6/7 1011111 | mutant=7/7 1111111` (pristine: `full=3/4`).
       Missing case: the package-rule floor boundary (the committed selftest only pins
       the Limits floor via `mut-limits-section-emptied`).
    4. X06-G2-head-10-lines (`head = body.splitlines()[:8]` -> `[:10]`).
       Witness: provenance trio pushed to lines 8-10 by five filler lines.
       `pristine=6/7 1011111 | mutant=7/7 1111111` (pristine: `verified-at=0 recheck=0`).
       Missing case: trio at lines 9-10 (the committed case pushes to 10-12, which the
       10-line window still misses).
    5. X07-G2-limits-anchor-grep-only (Limits anchor drops the `` `(?:grep|sed) ``
       alternative — the mutant is STRICTER). Witness: Limits keeps only the sweep
       command. `pristine=7/7 1111111 | mutant=6/7 1011111` (mutant: `anchored=0`).
       Missing case: a Limits section anchored by a backticked sweep command with no
       `S073.txt:N` cite — the selftest never exercises that documented alternative,
       so it could not notice the counter tightening it away.
    6. X10-G2-recheck-count-ge1 (exactly-one recheck line -> at-least-one).
       Witness: a second `recheck: cd ... --source S071` line appended.
       `pristine=6/7 1011111 | mutant=7/7 1111111` (pristine: `recheck=0`).
       Missing case: two recheck lines in one entry.
    7. X13-G3-locator-upper-bound-wide (`<= 589` -> `<= 100000`).
       Witness: registry anchor locator `L567-L590` (past the capture's 589 lines).
       `pristine=6/7 1101111 | mutant=7/7 1111111` (pristine: `bad=anchor-locator`).
       Missing case: a locator ending beyond the capture.
    8. X14-G3-cells-ge11 (`len(c) == 11` -> `>= 11`).
       Witness: S073 row with a twelfth cell. `pristine=5/7 1101110 | mutant=6/7 1111110`
       (pristine: `gate G3 pass=0 read=row-S073=absent-or-malformed`; G7 red in both —
       the census flags E01 on the same row).
       Missing case: an over-long registry row (G3's own verdict is untested; the
       committed case only drops a cell to ten).
    9. X20-G3-anchor-sha-prefix (`snap_sha not in row[5]` -> `snap_sha[:16] not in row[5]`).
       Witness: anchor cell carries the first 16 hex chars of the capture digest.
       `pristine=6/7 1101111 | mutant=7/7 1111111` (pristine: `bad=anchor-sha`).
       Missing case: a truncated sha in the anchor cell (the committed cases use a
       wrong 64-char value and a missing value — both still caught).
    10. X22-G4-quote-count-6 (`oks >= 8` -> `oks >= 6`).
        Witness: manifest repinned (grader-side `R46_PINS_OVERRIDE`, exactly as the
        committed selftest's repin cases do) with one non-core quote removed; 7 quotes
        still recheck OK. `pristine=6/7 1110111 | mutant=7/7 1111111`
        (pristine: `quotes-ok=7 frozen-cores-missing=0`).
        Missing case: a repinned manifest with 6-7 OK quotes (every committed
        quote-removal case trips the byte pin first, so the `oks` floor is never the
        deciding conjunct).
    11. X24-G4-core-prefix-match (`norm(c) not in mt` -> `norm(c)[:40] not in mt`).
        Witness: the AI-assistance core quote truncated to its first 40 chars (repinned).
        `pristine=6/7 1110111 | mutant=7/7 1111111` (pristine: `frozen-cores-missing=1`).
        Missing case: a core present only as a prefix.
    12. X26-G4-core-count-lenient (`not miss` -> `len(miss) <= 1`).
        Witness: the AI core replaced by another real capture line (anchor moved to 557
        so the quote still rechecks OK; repinned). `pristine=6/7 1110111 | mutant=7/7 1111111`
        (pristine: `frozen-cores-missing=1`).
        Missing case: exactly one frozen core missing while all eight quotes verify.
    13. X30-G5-single-curly-unquoted (single-curly >= 4-word quotes dropped from the
        uncited set). Witness: an uncited six-word `‘submit a report to the maintainer’`
        line. `pristine=6/7 1111011 | mutant=7/7 1111111` (pristine: `gate G5 pass=0`).
        Missing case: the committed probe uses a three-word single-curly quote, below
        the >= 4-word threshold, so the limb is never exercised.
    14. X33-G6-entry-size-2000 (entry floor 3000 -> 2000 bytes).
        Witness: a complete but compact entry (same four sections, same six located
        table rows, same cross-references) at < 3000 bytes.
        `pristine=6/7 1111101 | mutant=7/7 1111111` (pristine: `entry-bytes-ok=0`).
        Missing case: any entry whose byte size sits between the floor and the
        selftest's fixed 3600-byte pad.
    15. X35-G6-file-symlink-check-dropped (per-file knowledge symlink guard removed).
        Witness: a base knowledge file replaced by a symlink to a byte-identical copy
        under `corpus/notes/`. `pristine=6/7 1111101 | mutant=7/7 1111111`
        (pristine: `symlinks=1`).
        Missing case: a symlinked *non-entry* knowledge file (the committed symlink
        case only symlinks the F28 entry, which G1 already rejects).
    16. X36-G6-exempt-size-half (exempt entries may shrink to half).
        Witness: `claim-gates.md` cut from 6742 to 4000 bytes.
        `pristine=6/7 1111101 | mutant=7/7 1111111` (pristine: `exempt-entries-not-shrunk=0`).
        Missing case: a shrunk-but-not-deleted C1-exempt entry (the committed cases
        rename or delete it outright).
    17. X38-G7-sources-symlink-half (SOURCES.md symlink guard removed, corpus/ guard kept).
        Witness: `corpus/SOURCES.md` symlinked to a byte-identical `SOURCES-real.md`.
        `pristine=6/7 1111110 | mutant=7/7 1111111` (pristine:
        `gate G7 pass=0 read=census-input-is-a-symlink`).
        Missing case: a symlinked registry file.

F6. The 5 survivors with no witness — argued equivalent, not holes. For each I built
    the natural attacking input and the gate vectors came out identical
    (`witness_runner.py`: `DIFFERS=False`):
    - X08-G2-sections-count-len3: renamed section heading -> `pristine=6/7 1011111 |
      mutant=6/7 1011111`. `secs == 4` is subsumed by the separately-required
      `full == 4` (a renamed heading has no words, so full drops with it).
    - X25-G4-sha-ok-line-dropped: zeroed manifest sha -> `pristine=6/7 1110111 |
      mutant=6/7 1110111`. `source-recheck.py` exits non-zero on sha mismatch and only
      prints `S073:sha256 OK` after the hash matches, so `rc == 0` already implies the
      line; the conjunct is dead code.
    - X34-G6-nested-le-65: nested `.md` under `corpus/knowledge/` -> `pristine=6/7
      1111101 | mutant=6/7 1111101`. `everything == 65 and names == 65` already forces
      a flat directory, so `nested == 65` follows.
    - X40-G7-okline-anywhere and X41-G7-rc-only: census error row / missing registry
      -> both vectors `1101110`. The census emits `file<TAB>ok<TAB><path>` whenever it
      exits 0 (validate mode emits ok iff the lane had no E findings, and exit 0 iff no
      findings), so `rc == 0` implies the anchored ok line; both conjunct variants are
      subsumed. Caveat: this equivalence is argued against the census's current output
      vocabulary (verified on the fleet census output `file^Iok^I...`), not a formal
      proof over all possible census outputs.

F7. Battery cross-check. None of my 41 (old,new) pairs appears in the frozen
    `C2_MUTANTS` table (script check printed `drift-count: 0`, each `count=1`), and the
    frozen battery's own before-value reproduced independently of my work
    (`.ufo/waves/round-46/attempt2/controls/mutbat-before.txt`:
    `mutbat counter=c2 mutants=21 caught=8 equivalent=0 uncaught=13 baseline_failures=0`).
    My set is therefore additive evidence: the C1 extension must close not only the
    battery's 13 but also the 17 holes in F5 if the intent is that the committed
    selftest pins the counter.

# Limitations

- Graded against the committed selftest/counter at the lane tip I read
  (`ee03806b6b54a2822045e96641a77fa76984b410`; counter sha256
  `647bd5b7b62685519d8d396bf2d02eca7ad0bb440dd5c4041beabfaa45ea2909`,
  selftest sha256 recorded in `R46bMutSelfC2b.draft/selftest-sha256.txt`). If the C1
  seat has since extended the selftest, my survivors must be re-run against that
  extension; F5's witness trees are the reusable oracle for that re-run.
- Three G4 witnesses (X22/X24/X26) use the counter's documented grader-side
  `R46_PINS_OVERRIDE` re-pin, exactly as the committed selftest's repin cases do; under
  the strict pins those limbs are unreachable, which is itself part of the finding.
- X14's witness shows G3 flipping while G7 stays red (the census independently flags
  the same malformed row), so X14 is a hole in G3's own verdict, not in the overall
  pass/fail; the same caveat applies to no other survivor in F5 — the other sixteen
  produce a tree the pristine counter rejects outright and the mutant accepts outright.
- The do-nothing control run completed with failures>0 (output captured in
  `R46bMutSelfC2b.draft/dnc-control.log`); its exact tail line is quoted there. I did
  not re-run the full frozen battery (`r46-mutbat.py`) myself — the L1 asked for no new
  full battery passes — so my battery statement rests on the frozen receipt plus my
  independent baseline.
- No tooling was installed or upgraded; everything ran on the host's existing
  python3/bash/gawk (tooling directive: nothing to record).
- Scratch `$HYAKU_SCRATCH/kasegi-r46/R46bMutSelfC2b/` is removed on exit; all
  receipts named above are preserved in
  `.ufo/waves/round-46/attempt2/wave1/R46bMutSelfC2b.draft/`.
