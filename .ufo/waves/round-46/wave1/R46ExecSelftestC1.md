VERDICT: DRAFT-READY

Seat R46ExecSelftestC1 - counter selftest for C1 (frozen counter `corpus/instruments/r46-c1-gate.py`, sha256 prefix b0c730c834b4d7c6, unmodified: `git diff --quiet -- corpus/instruments/r46-c1-gate.py` -> clean).
Draft: `.ufo/waves/round-46/wave1/R46ExecSelftestC1.draft/r46-counters-selftest-c1.py` (stdlib, honours TMPDIR / `--work`, `--jobs`, `--keep`; builds everything under `$TMPDIR/c1st-*`, removes it at exit).

## What it builds and asserts
- BASE = copy of `/fast/scratch/hyaku/kasegi-r46/L1/pure` (the pure export is only read).
- TIP = another copy + `corpus/instruments/r46-c1-gate.py` copied in (the pure export predates the counter) + `claim-package-contract.md` (8 rows) and `claim-gates.md` (7 rows) each given `## Re-ground (round 46)`, rows anchored on `corpus/instruments/claim-package-check.py` and `corpus/instruments/fixtures/claim-package/exemplar/{evidence/manifest.json,custodian-receipts.json}`; line numbers are located in the committed bytes at build time; recheck line = `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/r46-c1-gate.py --entry corpus/knowledge/<entry>.md`.
- Every mutant = one recipe applied to a fresh copy of TIP (the recipe is printed with any non-OK case).

## Findings (final run, all quoted from the run, `real 1m53s` wall with --jobs 4)
1. TIP: `case TIP-7of7  L1=1 L2=1 L3=1 L4=1 L5=1 L6=1 L7=1 fixed=7/7 exit=0 verdict=OK` (the counter printed `c1-gate fixed=7/7 exit=0` on the synthetic tip; the harness asserts that line's numbers).
2. Do-nothing control (tree = baseline = pure): `case CONTROL-do-nothing  L1=0 L2=0 L3=0 L4=0 L5=0 L6=0 L7=1 fixed=1/7 exit=1 verdict=OK` - same 1/7 as the frozen control file.
3. Positive boundaries still 7/7 (counter does not over-reject): `P-exactly-six-rows ... fixed=7/7`, `P-prose-after-table ... fixed=7/7`, `X-stubbed-gate-copy-alone ... fixed=7/7` (a tree copy of the gate replaced by `sys.exit(0)` with valid rows reads 7/7 because L4/L6 run the counter's own bytes).
4. Rejected mutants (targeted limb read pass=0 and fixed<7), exact lines:
   - L1: `L1-recheck-line-deleted L1=0 ... fixed=6/7`; `L1-recheck-unparsable L1=0 ... fixed=6/7`; `L1-new-gated-entry L1=0 L2=0 ... fixed=5/7` (executing entry `ai-assisted-finding-validation.md` deleted/unparsable/`&& false`).
   - L2: `L2-only-one-reground L1=0 L2=0 ... fixed=5/7` (claim-gates line restored to BASE, section kept).
   - L3: `L3-line-has-tilde-path`, `L3-line-has-HOME-var`, `L3-line-names-other-entry`, `L3-line-softened-true`: each `L3=0 ... fixed=6/7`.
   - L5: `L5-body-line-deleted L5=0 fixed=6/7`; `L5-body-line-edited L5=0 fixed=6/7`.
   - L6: `L6-token-blanking-is-a-noop L6=0 fixed=6/7` (anchor file `######`, token `######`: blanking changes nothing, survivor).
   - L7: `L7-still-gated-line-edited L7=0 fixed=6/7`.
   - third gated entry: `X-third-gated-softened-true L3=0 L4=0 L5=0 L6=0 fixed=3/7`; `X-third-gated-line-deleted ... fixed=0/7` (counter exception path fails closed on all 7).
   - section only, lines left gated: `X-section-only-lines-kept fixed=1/7`.
   - anchor reached through a symlinked directory (`corpus/instruments/kn -> ../knowledge`, row anchors the entry itself): `X-anchor-self-via-symlinked-dir L4=1 L6=0 fixed=6/7` - the `rel == entry_rel` self-check is bypassed (L4 stays green), L6 is what rejects it.
   - Row-level breakage (row anchor moved, token absent, `|` in token, anchor is a symlink file, anchor outside the two dirs, five rows, one anchor file, duplicate row id, section twice): all read `L1=0 L2=0 ... L7=0 fixed=4/7` (the entry's own recheck line turns red so the entry drops back into the gated set; L1/L2/L7 catch it, L4 never sees it). With the tree's gate copy stubbed to `sys.exit(0)` (recheck line stays green) every one of them is caught by L4: e.g. `L4-row-anchor-moved+stubbed-gate-copy L4=0 fixed=6/7`, `L4-five-rows+stubbed-gate-copy L4=0 fixed=6/7`, `L4-anchor-is-symlink+stubbed-gate-copy L4=0 fixed=6/7`, `L4-duplicate-row-id+stubbed-gate-copy L4=0 fixed=6/7`, `L4-one-anchor-file+stubbed-gate-copy L4=0 fixed=6/7`.
   - Note: `L4-pipe-in-token` (token `api[_-]?key|secret|token|password`) is rejected: a `|` in a token cell splits the row (`row G2 ok=0 read=cells=7`) - an authoring trap, not a defect (use a token without `|`).

5. FALSE-GREENS - the frozen counter prints `c1-gate fixed=7/7 exit=0` on all of these (8 cases; each recipe = TIP + exactly this one edit):
   - F1 `L3-gate-incantation-in-comment`: contract recheck line `recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && true  # python3 corpus/instruments/r46-c1-gate.py --entry corpus/knowledge/claim-package-contract.md` -> `L3=1 ... fixed=7/7 exit=0`. L3 is a substring test (`"r46-c1-gate.py" not in ln`, `--entry corpus/knowledge/<e>` in ln, r46-c1-gate.py:187), so the gate name in a comment satisfies it while the line is `true`. Real rc of `bash -c 'true  # python3 ...'` = 0 (observed).
   - F2 `L3-gate-verdict-discarded-or-true`: real line + ` || true` -> 7/7.
   - F3 `L3-gate-verdict-discarded-semicolon`: claim-gates real line + ` ; true` -> 7/7.
   - F4 `L3-gate-only-echoed`: `recheck: cd <lane> && echo python3 corpus/instruments/r46-c1-gate.py --entry corpus/knowledge/claim-package-contract.md` -> 7/7.
   - F5 `L3-cd-target-not-the-lane`: `recheck: cd /fast/scratch/hyaku/kasegi-r46/no-such-dir && python3 corpus/instruments/r46-c1-gate.py --entry corpus/knowledge/claim-package-contract.md` -> 7/7, although run as written it fails (`bash -c 'cd /fast/scratch/hyaku/kasegi-r46/no-such-dir && true'` -> `No such file or directory`, rc=1, observed): the counter strips the `cd` (CD_RE, r46-c1-gate.py:61, applied at :187) and HOME_RE is applied only to the remainder, so the cd target is never validated.
   - F6 `L3-root-override-absolute`: real line + ` --root <absolute path of a scratch tree>` -> 7/7 (L3 never rejects `--root`; the line is grounded on a non-committed absolute path).
   - F7 `X-tautological-anchor-file`: new `corpus/instruments/r46-claim-note.txt` (four prose lines restating the claims) with claim-gates rows G1-G4 anchored there -> `L4=1 L6=1 ... fixed=7/7`. Inherent: the counter cannot tell an anchor written for the purpose from real implementation bytes (the kill_rule's non-author reading is the only check).
   - F8 `X-rows-inside-code-fence`: contract's table wrapped in a ``` fence -> 7/7 (section_rows is not markdown-aware; the fenced rows still count).
   F1-F6 are all "the recheck line stops executing the gate but still counts as un-gated", exploitable because the aggregate counter measures `exit 0 + a substring`, not "this line runs the gate and propagates its status". A fullmatch on `cd <lane> && python3 corpus/instruments/r46-c1-gate.py --entry corpus/knowledge/<e>.md` (no `--root`, no trailing operator/comment) would close F1-F6; F7/F8 need a non-author reading / a fence check.

## Final line
`selftest cases=47 failures=8` (the 8 failures are exactly F1-F8; 47 = TIP + control + 42 mutants/stub variants + 3 positive boundaries; every other case OK, 0 UNEXPECTED).

## Limitations
- One run of the final harness at lane HEAD; earlier runs (twice) read the same TIP 7/7 and control 1/7; I did not repeat the whole suite for flakiness.
- Mutants break the synthetic tip, not the real lane tip; the seat does not know the L1 landing's actual rows, so rows/line numbers are mine.
- The counter treats a tree's recheck lines as run on this host (`~/Projects/bounties` absent -> 24 gated at BASE); on a host where it exists the BASE classification would differ and `EXEC_ENTRY` (`ai-assisted-finding-validation.md`) must still execute.
- `--jobs 4` parallel; heavy (user 7m45s in the first run).
- No tools installed, no git mutation, fleet repo untouched, scratch dir removed on exit.
