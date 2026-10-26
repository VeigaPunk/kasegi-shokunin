# ExecFRLimbs — round 31 receipt (FR limbs of C1)

Seat: ExecFRLimbs. Owned paths: `corpus/instruments/frontier-recheck-count.py`,
`corpus/instruments/limb-fixtures/fr/**`,
`.ufo/waves/round-31/wave1/ledger-fragments/fr.json`, this receipt.
Lane root `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, base
`b374febbb33ccadade78a787279707fd5d2e6e1d`. Environment: Python 3.14.8, lane HEAD
`8a8916c` (read-only), 2026-10-25T23:40Z. Answering model per the runtime route:
`devin/deepseek-v4-1-flash` (no model passed by this seat). Tool installs: none
(nothing needed; stdlib only, no pacman transaction run).

## Outcome

Both assigned limbs are **killed**, each by its own isolating fixture root under
`corpus/instruments/limb-fixtures/fr/`, and the fragment is verified against the
landed counter:

```
$ python3 corpus/instruments/limb-mutation-check.py --ledger .ufo/waves/round-31/wave1/ledger-fragments/fr.json
LIMB FR-missing-entry live=1/y mutant=1/n verdict=killed
LIMB FR-duplicate-entry live=1/y mutant=0/n verdict=killed
limbs=2 killed=2 survivors=0
controls=0 rejected=0
frag_counter_exit=0
```

Instrument bytes **unchanged** — no strengthening was needed, the limbs are
load-bearing on the landed bytes once a fixture-backed kill command exists:

```
$ sha256sum corpus/instruments/frontier-recheck-count.py
aa60b58126569a1c8ec04409011df5f6225a9c18f2a77ea6410cd1d0d5dc0893  corpus/instruments/frontier-recheck-count.py
```

That digest equals the base digest quoted in `claims.json` C1
`do_nothing_control` (`frontier-recheck-count.py aa60b581…`), so the instrument
is byte-identical to the frozen base; the round's work on this limb set is the
fixtures + kill commands, not an instrument edit.

## Files written

| path | sha256 | bytes |
|---|---|---|
| `corpus/instruments/limb-fixtures/fr/NOTE.txt` | `e9398fc5f33235c500e9caffa5217c0ff851b0cf8e00bb2eef4c545b13c44e09` | 1193 |
| `corpus/instruments/limb-fixtures/fr/fr-missing-entry/corpus/README.md` | `9376e3316b0f61d1b37d5d049a926cf24443f838effa10db715b550bd05f1542` | 250 |
| `corpus/instruments/limb-fixtures/fr/fr-duplicate-entry/corpus/README.md` | `43607e43caee090f3a82b812eb17121613f98abd9c51b46822e8e8246d088c80` | 331 |
| `corpus/instruments/limb-fixtures/fr/fr-duplicate-entry/corpus/knowledge/dup-entry.md` | `9e46bb180f0dd8ef42858c8dc5a7914c906c7843d7ce41f4cd0e6779289370db` | 335 |
| `corpus/instruments/limb-fixtures/fr/fr-duplicate-entry/corpus/source-snapshots/round-24/manifest.json` | `b32443bbec478c34342ef25ef01cb87dfa6c2a3369a913d8f21b47238ccb601e` | 303 |
| `corpus/instruments/limb-fixtures/fr/fr-duplicate-entry/corpus/source-snapshots/round-24/S003.txt` | `1054e187e7ce514dcd3b7b50954f4245ee112c85977506840464c238189cee0d` | 68 |
| `.ufo/waves/round-31/wave1/ledger-fragments/fr.json` | `ebda80f6a7c37138d37fe6c39045a97d5609efc08f15acfa10691ab7643cfc1b` | 2490 |

Whole fixture tree is 2480 B of committed evidence (R14: no corpus copy — the
only capture bytes are the 68 B `S003.txt` and its 303 B manifest, reused from
the round-30 fixture, digest identical to the round-30 original).

## A. Live runs (unmutated instrument, landed fixture roots)

```
$ python3 corpus/instruments/frontier-recheck-count.py --root $PWD/corpus/instruments/limb-fixtures/fr/fr-missing-entry
FAIL     F98  knowledge/zz-missing.md                              ids=-              exit=-    problems=missing-entry
entries=1 pass=0 exit=1
exit=1

$ python3 corpus/instruments/frontier-recheck-count.py --root $PWD/corpus/instruments/limb-fixtures/fr/fr-duplicate-entry
PASS     F98  knowledge/dup-entry.md                               ids=S003           exit=0   
PASS     F97  knowledge/dup-entry.md                               ids=S003           exit=0   
DUPLICATE-ENTRY F98,F97 knowledge/dup-entry.md
entries=2 pass=2 exit=1
exit=1
```

Isolation (R13 — each fixture fails exactly one limb and no other):

- `fr-missing-entry` has one admitted row and its only problem token is
  `problems=missing-entry`; no other problem class is reachable, and the run
  prints the row id `F98` with **no traceback**.
- `fr-duplicate-entry` has both rows **PASS** their own A–D contract
  (`ids=S003 exit=0` each, real `source-recheck.py` invocation, exit 0), so the
  `DUPLICATE-ENTRY F98,F97` line is the sole reason the run exits 1. The fixture
  is self-contained: the recheck line is
  `python3 ../../../source-recheck.py --manifest corpus/source-snapshots/round-24/manifest.json --source S003`,
  resolved relative to the fixture root, so it holds inside the counter's
  scratch copy and carries no absolute lane path.

## B. Ledger rows (as written to `fr.json`)

```
FR-missing-entry
  find    : "    if not os.path.isfile(full):\n        return None\n"   (occurs 1x)
  replace : ""
  kill    : python3 {inst} --root {root}/corpus/instruments/limb-fixtures/fr/fr-missing-entry
  live_exit: 1
  signal  : FAIL\s+F98\s+knowledge/zz-missing\.md\s+ids=-\s+exit=-\s+problems=missing-entry\nentries=1 pass=0 exit=1\n?

FR-duplicate-entry
  find    : the seen_realpath / DUPLICATE-ENTRY / fail_closed block (occurs 1x)
  replace : "    fail_closed = not records or passed != len(records)\n"
  kill    : python3 {inst} --root {root}/corpus/instruments/limb-fixtures/fr/fr-duplicate-entry
  live_exit: 1
  signal  : PASS\s+F98\s+knowledge/dup-entry\.md\s+ids=S003\s+exit=0[ \t]*\nPASS\s+F97\s+knowledge/dup-entry\.md\s+ids=S003\s+exit=0[ \t]*\nDUPLICATE-ENTRY F98,F97 knowledge/dup-entry\.md\nentries=2 pass=2 exit=1\n?
```

Find-count check on the landed bytes (both exactly once; the bare
`if not os.path.isfile(full):` occurs 3x, so the two-line form with
`return None` is the unique anchor):

```
$ python3 - (count of each find in corpus/instruments/frontier-recheck-count.py)
guard 1
dupblock 1
ifisfile 3
```

Signal regexes match the live output under **both** `re.search` and
`re.fullmatch` (so the row survives either matcher choice in the counter):

```
fr-missing-entry live exit 1 search True fullmatch True
fr-duplicate-entry live exit 1 search True fullmatch True
```

## C. Red-before (measured, not asserted)

C1. Without the fixtures under `corpus/` the rows cannot even establish a live
baseline — the round-30 roots live under `.ufo/waves/round-30/c1-controls/`,
outside the counter's `<root>/corpus` copy:

```
$ python3 corpus/instruments/limb-mutation-check.py --ledger /tmp/fr-prefixture.json
LIMB FR-missing-entry-PRE live=2/n mutant=-/- verdict=invalid:live-baseline
LIMB FR-duplicate-entry-PRE live=2/n mutant=-/- verdict=invalid:live-baseline
limbs=2 killed=0 survivors=0
controls=0 rejected=0
pre_exit=1
```

This is why the fixtures had to land under `corpus/instruments/limb-fixtures/fr/`
(the contract's kill template) rather than being cited in place.

C2. Mutant runs, applied to a scratch copy of the instrument (lane bytes
untouched), each mutant compiled with `py_compile` before running:

```
find counts 1 1
mut-A-missing-entry sha256 013dd1e537a439e1cb19f2cf9b44141c84190d799f8e3d016cd6eec5f0cfd5b5 compiles=True bytes 9363
mut-B-duplicate     sha256 5028f09e2ee8cb9d46c615adc15c2b4f8d5c8fce96b0f31ddbcbaf45d287a7bb compiles=True bytes 8978
---- mut-A-missing-entry on fr-missing-entry exit=1
Traceback (most recent call last):
  ...
  File ".../mut-A-missing-entry.py", line 79, in entry_contract
    with open(full, encoding="utf-8") as fh:
FileNotFoundError: [Errno 2] No such file or directory: '.../fr-missing-entry/corpus/knowledge/zz-missing.md'
---- mut-A-missing-entry on fr-duplicate-entry exit=1
PASS     F98  knowledge/dup-entry.md                               ids=S003           exit=0   
PASS     F97  knowledge/dup-entry.md                               ids=S003           exit=0   
DUPLICATE-ENTRY F98,F97 knowledge/dup-entry.md
entries=2 pass=2 exit=1
---- mut-B-duplicate on fr-missing-entry exit=1
FAIL     F98  knowledge/zz-missing.md                              ids=-              exit=-    problems=missing-entry
entries=1 pass=0 exit=1
---- mut-B-duplicate on fr-duplicate-entry exit=0
PASS     F98  knowledge/dup-entry.md                               ids=S003           exit=0   
PASS     F97  knowledge/dup-entry.md                               ids=S003           exit=0   
entries=2 pass=2 exit=0
```

Cross-mutant matrix = isolation proof: mut-A leaves the duplicate fixture's
output **byte-identical** (same exit 1, same lines), and mut-B leaves the
missing-entry fixture's output **byte-identical**; each fixture therefore
depends on exactly one limb.

C3. Signal verdicts on the mutants:

```
mut-A on fr-missing-entry mutant_exit= 1 sig_search= False sig_fullmatch= False
mut-B on fr-duplicate-entry mutant_exit= 0 sig_search= False sig_fullmatch= False
```

`FR-missing-entry` is killed **by signal only** (the mutant still exits 1 via an
uncaught `FileNotFoundError`), which is exactly the failure mode
`MutFRExisting` flagged: an exit-code-only kill would let the traceback
survive. The row's signal is the printed row id + `problems=missing-entry` +
the summary line, none of which a traceback produces.

## D. Counter-semantics replay (scratch lane, mirroring the counter)

One-limb replay in a `mktemp` lane copy of `corpus/`, kill commands substituted
and run with `bash -c` at cwd = scratch root:

```
LIMB FR-missing-entry     live=1/y mutant=1/n verdict=killed findcount=1 noop=False compiles=True
   live out: FAIL     F98  knowledge/zz-missing.md ... problems=missing-entry | entries=1 pass=0 exit=1
   mut  out: Traceback (most recent call last): |   File "/tmp/frsim-.../corpus/instruments/frontier-recheck-count.py", line 226 ...
LIMB FR-duplicate-entry   live=1/y mutant=0/n verdict=killed findcount=1 noop=False compiles=True
   live out: PASS F98 ... | PASS F97 ... | DUPLICATE-ENTRY F98,F97 knowledge/dup-entry.md | entries=2 pass=2 exit=1
   mut  out: PASS F98 ... | PASS F97 ... | entries=2 pass=2 exit=0
```

The duplicate fixture's relative `../../../source-recheck.py` resolves inside the
scratch copy (live `exit=0` per row), so the kill command is scratch-hermetic.

## E. Real lane harness — PRE-STATE, non-comparative (M30-3)

Run while F15/registry seats were mid-edit; label PRE-STATE, do not compare to
any after-column. Re-run belongs to the L1 closure (target after F15 lands:
`entries=18 pass=18 exit=0`).

```
$ python3 corpus/instruments/frontier-recheck-count.py
PASS     F01  knowledge/cvss-v4-severity-and-vector.md             ids=S001           exit=0
... (16 more PASS lines, F14 last)
entries=17 pass=17 exit=0
harness_exit=0
```

## F. No collateral on the two instruments that walk `corpus/`

`recheck-audit.py` globs `corpus/knowledge/*.md` only (single-level) and never
enters the fixture tree — receipt JSON shows no fixture path among its 44
records:

```
$ python3 corpus/instruments/recheck-audit.py --quiet     # PRE-STATE, F15 entry in flight
strict pass=44/44 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=20 gated=24 broken=0
lines=44 total=44 pass=44 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=1
expect=present expected=43 missing=0 unexpected=1 exit=1
audit_exit=1
$ (glob vs expected diff)
glob count 44 expected count 43
unexpected: ['corpus/knowledge/vendor-third-party-finding-coordination.md']
missing: []
```

The single `unexpected=1` is ExecEntryF15's new entry (not yet in
`knowledge-expected.txt`), i.e. an in-flight PRE-STATE observation owned by
another seat — **not** caused by this seat: `recheck-audit.py` cannot see the
fixtures (`no fixture paths in audit`).

`resolve.py` walks all of `corpus/**/*.md`, so the fixtures were built with **no
backtick tokens** (`grep -rn '`' corpus/instruments/limb-fixtures/fr/` → none).
Measured via `resolve.collect` on the lane vs an identical copy with the fr tree
removed:

```
cites_real 2201 cites_base 2201 identical True
added 0 removed 0
occurrences real 4311 base 4311
files scanned-with-cites real 85 base 85
```

The round-18 census of record is unchanged by this tree. (First attempt at this
measurement showed a 326-citation delta; cause was the comparison copy missing
`SKILL.md`, whose citations are all in that delta — re-measured with `SKILL.md`
present, delta 0.)

## G. Lane state

Read-only `git status --porcelain` after the work: `frontier-recheck-count.py`
is not modified; the only new paths from this seat are
`corpus/instruments/limb-fixtures/` (fr subtree) and
`.ufo/waves/round-31/wave1/ledger-fragments/fr.json` plus this receipt. The
counter ran scratch-only and left no `__pycache__` or temp file in the lane. No
git/jj mutation was run by this seat.

## Risks / notes

1. **Signal padding coupling.** Both signals encode the harness' `%-13s`/`%-4s`
   column padding (tolerated with `\s+` and `[ \t]*`). A future change to the
   print format invalidates the rows by making them `invalid:live-baseline`, not
   by silently passing — fail-closed, but it does couple the ledger to the
   format. Any format change must re-measure these two rows.
2. **Advisory, out of ledger scope (do not widen the frozen 13).**
   `MutFRExisting` reports two harness mutants that no current oracle kills
   (dropping `no-source-selection`; dropping the `not-a-recheck-invocation`
   branch). The frozen limb set is 13, so they are not ledger rows; the two
   one-line fixtures that would isolate them are described in that receipt and
   are not landed by this seat.
3. **`live_exit 1` is correct, not a defect.** Both FR limbs protect a
   fail-closed exit 1; the counter's rule (`exit != live_exit` OR signal
   mismatch) is what makes the verdict meaningful. An attack seat should not
   read `live=1` as "the baseline already fails".
4. **No blockers.** No peer receipt was needed; nothing was waited on.
