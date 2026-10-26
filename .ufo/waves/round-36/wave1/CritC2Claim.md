# CritC2Claim — causal separability of the C2 counters (round 36, coverage)

Verdict: **the do-nothing control is sound; the counters are not causally separable as measurements, and three of
them individually accept a decoy.** Concretely, on scratch trees exported from the base commit:

1. **Do-nothing control holds.** Untouched base export `cc692008` (and, as a second control, the claims-freeze head
   `b47f2cdf`) prints every before value — `frontier=18 registry=52 cite53=0 knowledge=47 harness=entries=21 pass=21
   exit=0 sr53_exit=2 binding_exit=0 census_exit=0 (W04 S028/S029 only)` — and falls short of the after target on
   **all six** counters. It cannot satisfy C2.
2. **No single move reaches the after target; the conjunction does.** Eleven single-move trees were measured; each
   moves only its own counter (plus its documented dependents) and no single move produces the after vector. The
   full move (`m6`) does: `19/53/1/48`, `entries=22 pass=22 exit=0`, `PASS F19 ids=S053`, `sr53_exit=0`,
   `binding_exit=0`, `census_exit=0`.
3. **But `entries=22`, `knowledge=48` and `entries=22 pass=22 exit=0` are decoys, and the harness F19 line is not
   export-pinned.** `entries=22` ships with `pass=21 exit=1` when only the frontier row is added; `entries=22
   pass=22 exit=0` ships with **no F19 row at all** when an existing row is given a second passing entry; and with
   the *drafted* F19 `recheck:` line (`cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && …`, ScribeEntryF19.md:146)
   the harness prints `PASS F19 ids=S053` on an export that contains **zero S053 capture bytes** (`m7`, `m8`).
   Only the export-local `source-recheck --source S053` refuses (`m8`: `sr53_exit=2`; with a root-relative recheck
   line the same tree fails the harness too, `m9`: `entries=22 pass=21 exit=1 problems=recheck-exit-2`).

Impact on the claim as frozen: C2's *predicate* survives, because it quotes the `PASS F19 ids=S053` line and keeps
`source-recheck S053 exit 0` in both the counter list and the kill rule. What does **not** survive is reading the
counter vector as independent evidence: `entries=`, `pass=`, `knowledge=`, and (per `m8`) `binding_exit=0` are each
satisfiable without the artifact they are supposed to witness. See §5 for the smallest corrections.

## 1. Method

- Base export: `git archive cc692008b0cfd58d18275aa6c4aed79620120799 | tar -x -C $S/base`; second control:
  `git archive b47f2cdf17d9f6021cbdb4db1add09a9dbf4f1d6` (`$S/head-frozen`). No `.git` in either tree.
- One move per tree, built by `$S/build.py` from the base export; every other artifact byte-frozen:
  `m1` frontier row only · `m2` registry row only, planned shape (anchor cites the round-36 capture, `used-by` names
  the new entry) · `m2b` registry row only, `used-by = —` · `m3` entry file only · `m3b` an *unrelated* knowledge
  entry only · `m4` capture + manifest only · `m5` harness decoy (second passing entry appended to the existing F18
  row; nothing else touched) · `m6` all four planned moves · `m7` frontier row + entry with the drafted
  `cd <other tree> &&` recheck line, no capture in the tree · `m8` `m7` + registry row · `m9` `m8` with a
  root-relative recheck line.
- Counter vector (`$S/measure.sh`, one line per tree): the five frozen greps, `python3
  corpus/instruments/frontier-recheck-count.py --root <tree>`, `python3 corpus/instruments/source-recheck.py
  --manifest corpus/source-snapshots/round-36/manifest.json --source S053`, `python3
  corpus/instruments/capture-binding-check.py --root <tree>`, and
  `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <tree>/corpus/SOURCES.md --today
  2026-10-26`. Full transcript: `$S/matrix.txt` (sha256 `c980646a118c718782ddd3a98fd733608f13f2a6155fb1fa715cfae62f0846f4`).
- Scratch only, under `/fast/scratch/hyaku/kasegi-r36/CritC2Claim`; no lane write, no fleet write, no tooling
  installed. Lane `git status --porcelain` after the run shows only the L1's own untracked
  `.ufo/waves/round-36/` files.

## 2. Matrix

| tree (one move) | frontier | registry | cite53 | knowledge | harness | sr53 | binding | census |
|---|---|---|---|---|---|---|---|---|
| base `cc692008` (do nothing) | 18 | 52 | 0 | 47 | `21/21 exit=0` | 2 | 0 | 0 |
| head `b47f2cdf` (do nothing) | 18 | 52 | 0 | 47 | `21/21 exit=0` | 2 | 0 | 0 |
| `m1` frontier row | **19** | 52 | 0 | 47 | `entries=22 pass=21 exit=1`, `FAIL F19 … missing-entry` | 2 | 0 | 0 |
| `m2` registry row (planned) | 18 | **53** | 0 | 47 | `21/21 exit=0` | 2 | 0 | **1** `E11 S053 missing used-by` |
| `m2b` registry row (`used-by —`) | 18 | **53** | 0 | 47 | `21/21 exit=0` | 2 | 0 | 0 (`W03 S053 mined but unused`) |
| `m3` entry only | 18 | 52 | **1** | **48** | `21/21 exit=0` | 2 | 0 | 0 |
| `m3b` unrelated entry only | 18 | 52 | 0 | **48** | `21/21 exit=0` | 2 | 0 | 0 |
| `m4` capture+manifest only | 18 | 52 | 0 | 47 | `21/21 exit=0` | **0** | **1** (`no-row`) | 0 |
| `m5` harness decoy only | 18 | 52 | 0 | 47 | **`22/22 exit=0`**, no F19 line | 2 | 0 | 0 |
| `m6` all four moves | **19** | **53** | **1** | **48** | **`22/22 exit=0`**, `PASS F19 ids=S053` | **0** | **0** | 0 |
| `m7` cd-recheck, no capture | **19** | 52 | **1** | **48** | **`22/22 exit=0`**, `PASS F19 ids=S053` | **2** | 1 | 0 |
| `m8` cd-recheck + row, no capture | **19** | **53** | **1** | **48** | **`22/22 exit=0`**, `PASS F19 ids=S053` | **2** | **0** | **0** |
| `m9` root-relative recheck, no capture | **19** | **53** | **1** | **48** | `entries=22 pass=21 exit=1`, `FAIL F19 exit=2 recheck-exit-2` | 2 | 0 | 0 |

`binding`/`census` are exit codes; bold marks a counter that moved off its before value.

## 3. What separates and what does not

- **`frontier` is a clean single counter among the greps.** `m1` moves 18→19 and none of the other three grep
  counters (registry, cite53, knowledge) moves; only the derived harness `entries` follows it.
- **`registry` is separable only if its row is weakened.** In the planned shape the row names its `used-by` entry, so
  `m2` alone is `census_exit=1 / E11 S053 missing used-by` — the registry counter cannot be moved without the entry
  file. The isolated variant `m2b` ( `used-by = —` ) is `census_exit=0` but adds `W03 S053 mined but unused`.
  Consequence: "registry rows=53" is only census-clean *together with* the entry, and a 53-row reading accompanied by
  `W03 S053` is a mined row nothing uses.
- **Row placement is load-bearing.** Appending the S053 row after the file's last `##` section is
  `E12 S053 row outside Registry section` (my first `m2`); the row must land inside the Registry table (before the
  section ends). `E12` fires on placement alone, so an integrator who appends at EOF gets `census_exit=1` with an
  otherwise valid row.
- **The entry moves two counters at once and the count is decoyable.** One file moves `cite53` 0→1 *and*
  `knowledge` 47→48 — they are two readings of one artifact, not two witnesses. `m3b` shows `knowledge=48` with
  `cite53=0`: the knowledge count accepts any added `.md`, so it is not evidence of the citation.
- **`sr53` is separable from the row but `binding` is not separable from either.** `m4` gives `sr53_exit=0` with
  `binding_exit=1 rule=no-row`: a capture plus a self-consistent manifest passes the quote check with no registry row
  at all. Capture-binding is the conjunction (record ∧ row ∧ URL ∧ provenance), never a single-move counter.
- **`entries` and `pass` are derived counters, not free ones.** `entries` is a function of the README rows
  (`m1`: 21→22 with no entry on disk), and `pass` is a conjunction over frontier ∧ entry ∧ capture ∧ manifest.
  `m5` is the decisive decoy: an extra *passing* entry appended to the existing F18 row prints
  `entries=22 pass=22 exit=0` with `frontier=18 registry=52 cite53=0 knowledge=47` and **no F19 line at all**. So
  `entries=22 pass=22 exit=0` is reachable without any part of the F19 admission.

## 4. The harness counter is not export-pinned (material defect)

The harness executes each entry's `recheck:` line as `bash -c <line>` with `cwd=<root>`
(`frontier-recheck-count.py:224`), but **46 of the 47** committed knowledge entries begin their recheck line with
`cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && …`; the 47th is a non-instrument `test ! -e` line. Any such
line re-anchors the check to the **live lane**, so a harness run over a `git archive` export measures the live lane
for those entries, not the export. Demonstrated directly:

```
$ cp -a base d0_export_bytes_stripped; rm d0_export_bytes_stripped/corpus/source-snapshots/round-35/S052.txt
$ (cd d0_export_bytes_stripped && python3 corpus/instruments/frontier-recheck-count.py --root .) | tail -1
entries=21 pass=21 exit=0                       # F18 still PASSes although its capture is gone from the tree
$ (cd d0_export_bytes_stripped && python3 corpus/instruments/source-recheck.py \
      --manifest corpus/source-snapshots/round-35/manifest.json --source S052); echo exit=$?
S052:source UNAVAILABLE reason=missing
exit=2
```

The drafted F19 entry carries the same prefix — `recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin &&
python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-36/manifest.json --source S053`
(`wave1/ScribeEntryF19.md:146`, re-verified in `wave1/ExecC2QuoteOnce.md:107`) — so after integration its PASS is a
live-lane property too. `m7`/`m8` are the emulation (the `cd` target holds the bytes; the measured tree does not):

- `m8`: `frontier=19 registry=53 cite53=1 knowledge=48`, `entries=22 pass=22 exit=0`, `PASS F19 ids=S053`,
  `src-recheck S053 exit 0`, `capture-binding exit 0`, `census exit 0` — **and the tree's
  `corpus/source-snapshots/round-36/` holds only `manifest.json`**. The manifest asserts a sha256 for bytes that are
  not in the export, and capture-binding still exits 0: its rules bind *files present* to records and records to
  rows/URL/provenance, and nothing binds a record's `path` to a file that exists (that limb is `source-recheck`'s
  sha256 alone). Seven of the eight after-target readings are met with no capture bytes in the tree; only the
  export-local `source-recheck --source S053` refuses (`exit=2`).
- `m9` pins the cause: identical tree, recheck line written root-relative (no `cd`), and the harness flips to
  `entries=22 pass=21 exit=1`, `FAIL F19 … exit=2 problems=recheck-exit-2`.

## 5. Smallest safe corrections

1. **F19 entry, one line:** drop `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && ` from the `recheck:` line;
   keep `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-36/manifest.json
   --source S053`. The harness already runs with `cwd=<root>`, so on the lane the relative form resolves identically
   and on an export it becomes export-pinned (`m9`). No instrument change, no convention change beyond this entry.
2. **Quote the binding clause, never the bare counts.** C2's receipt must quote the `PASS F19
   ids=S053` line verbatim; `entries=22` alone is `pass=21 exit=1` (`m1`) and `entries=22 pass=22 exit=0` alone is
   reachable with no F19 row (`m5`). Likewise report `cite53=1`, not `knowledge=48` alone (`m3b`).
3. **Land order and placement:** entry file before the registry row (`E11` otherwise), row inserted inside the
   Registry table (`E12` otherwise). Do not read `binding_exit=0` as "the capture bytes exist" — that reading needs
   the export-local `source-recheck --source S053` exit.

## 6. Impacted axes

- `coverage` (C2): counter independence is overstated as frozen. The predicate and kill rule survive because they
  name the F19 line and `source-recheck S053`; the "counters move independently" reading does not.
- `depth:verifiability` (C1): adjacent, not mine to land — the same `cd`-escape makes any export-level harness
  reading of inherited entries a live-lane reading (46/47 lines). Flagged for the C1 seats; no C1 claim depends on
  the harness today (`r36-closure.sh` E1-E9 does not include it).
- `depth:density`: no counter in this claim touches it; no impact observed.

## 7. Tooling

None installed or upgraded. Tools used: `bash`, `git` (read-only: `archive`, `rev-parse`, `status`), `python3`
(stdlib), `grep`/`wc`/`sha256sum`, the lane's own instruments, and the fleet read-only
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`. Scratch removed after this receipt was written.

Report: `.ufo/waves/round-36/wave1/CritC2Claim.md`
