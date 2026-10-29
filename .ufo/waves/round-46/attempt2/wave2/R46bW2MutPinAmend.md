VERDICT: BROKEN

# R46bW2MutPinAmend — r46-c2-gate.py v1.3 ledger exemption, verified with mutants

Scope: item "if v1.3 landed, verify with mutants: shrunk / stubbed / swapped-name ledger must each turn G6 red; v1.2 bytes at eb874bc must read 7/7 on the era export."
v1.3 landed (tip `96379ae`, `corpus/instruments/r46-c2-gate.py`, sha256 `29d50bf0a3c24ae182257ad225c34aa3d241af4345c09a4eca6f3a949e335d1c`; `CONTENT_EXEMPT` includes `considerthese-proposals-ledger.md`; `EXEMPT_BASE_SIZE` ledger = 30696). The ledger row was therefore not a deferral case.

Summary:
- The three named mutants do turn G6 red (holds). The v1.2 bytes at `eb874bc` read 7/7 (holds).
- The stated "bytes may grow never shrink" is NOT enforced at the wave-1 tip size: a truncation that removes about 10 KB of the wave-1 ledger dispositions (40843 -> 31000 bytes) reads G6 green (counterexample, finding 2).
- The ledger content itself is not pinned: a byte-flip plus one appended byte, or a 31000-byte junk replacement, reads G6 green (finding 3).
- At the tip G6 is red for a reason unrelated to the ledger (the F29 entry as the 66th file), so the ledger mutants only discriminate on the `eb874bc`-era baseline (finding 1).

## Environment and method

- Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (`git rev-parse --show-toplevel` confirmed). Tip `HEAD` = `96379ae26ef9443097b860ddb33ef924b2cd5b5a`.
- Exports (`git archive ... corpus | tar -x`) into scratch `kasegi-r46/R46bW2MutPinAmend/`:
  - `era/` = `eb874bc` corpus (the v1.2 era; `knowledge` = 65 files; ledger 30696 bytes; sha256 of v1.2 `r46-c2-gate.py` = `647bd5b7b62685519d8d396bf2d02eca7ad0bb440dd5c4041beabfaa45ea2909`).
  - `tip/` = `HEAD` corpus (`knowledge` = 66 files).
- Gate under test is copied into `era/corpus/instruments/r46-c2-gate-v13.py` so `TOOL_ROOT` resolves to the fixture (the script locates `source-recheck.py` from its own path).
- Each mutant is a fresh `tar` copy of `era/corpus` with one change applied. Output filtered to the G6 line and the summary line.
- Scratch removed on exit (see the final section).

## Finding 0 — the tip is red on G6, and the red is caused by the F29 entry, not the ledger

Command: `python3 corpus/instruments/r46-c2-gate.py --root <live lane>`
```
gate G1 pass=0 read=rows=29 admitted=29 dup=0
gate G6 pass=0 read=knowledge=66 entries=66 nested-md=66 base-intact=0 entry-bytes-ok=1
c2-gate fixed=5/7 exit=1
```
Attribution: copy of the tip with ONLY `corpus/knowledge/github-repository-security-advisories.md` removed (ledger left at the grown HEAD size):
```
gate G6 pass=1 read=knowledge=65 entries=65 nested-md=65 base-intact=1 entry-bytes-ok=1
c2-gate fixed=5/7 exit=1
```
So G6 red at the tip = the 66th file (F29 entry), which the frozen C2 counter does not expect. It is the deferral E3 already records ("At THIS round's tip the v1.3 counter reads 5/7 (G1 28->29, G6 65->66)"). The report must carry it: the tip 5/7 is not evidence about the ledger; the grader for the after-state is `r46-f29-gate.py`.

## Finding 1 — named mutants: HOLD (discriminated against do-nothing control)

Baseline (era export, v1.3 bytes), full gate: `gate G6 pass=1 read=knowledge=65 entries=65 nested-md=65 base-intact=1 entry-bytes-ok=1` and `c2-gate fixed=7/7 exit=0`.

| case | ledger change | G6 line (verbatim) | c2 |
|---|---|---|---|
| ctl-noop (do-nothing control) | none | `pass=1 read=knowledge=65 ... base-intact=1 entry-bytes-ok=1` | 7/7 exit=0 |
| ctl-HEAD-grown | replaced by HEAD ledger (40843 bytes) | `pass=1 ... base-intact=1` | 7/7 exit=0 |
| ctl-base-file-byte | (ledger untouched) `printf x >>` `ai-assisted-finding-validation.md` | `pass=0 read=... base-intact=0 entry-bytes-ok=1` | 6/7 exit=1 |
| ctl-extra-nonmd | `knowledge/notes.txt` added | `pass=0 read=knowledge=65 entries=66 nested-md=65 base-intact=0` | 6/7 exit=1 |
| **shrunk** -> 30695 bytes (1 below floor) | `head -c 30695` of era ledger | `pass=0 read=symlinks=0 exempt-entries-not-shrunk=0` | 6/7 exit=1 |
| **shrunk** -> 20000 bytes | `head -c 20000` | `pass=0 read=symlinks=0 exempt-entries-not-shrunk=0` | 6/7 exit=1 |
| **stubbed** text | `printf 'stub\n'` | `pass=0 read=symlinks=0 exempt-entries-not-shrunk=0` | 6/7 exit=1 |
| **stubbed** empty | `: >` | `pass=0 read=symlinks=0 exempt-entries-not-shrunk=0` | 6/7 exit=1 |
| **swapped-name** rename | ledger -> `considerthese-ledger.md` | `pass=0 read=symlinks=0 exempt-entries-not-shrunk=0` | 6/7 exit=1 |
| **swapped-name** ledger <-> claim-gates (bytes follow names) | sizes 15372 under ledger name | `pass=0 read=symlinks=0 exempt-entries-not-shrunk=0` | 6/7 exit=1 |
| swap bytes ledger <-> ai-assisted-finding-validation.md | ledger name holds 4866 bytes | `pass=0 read=symlinks=0 exempt-entries-not-shrunk=0` | 6/7 exit=1 |
| rename claim-gates only | `claim-gates.md` -> `claim-gates-old.md` | `pass=0 read=symlinks=0 exempt-entries-not-shrunk=0` | 6/7 exit=1 |

Note on the label: `exempt-entries-not-shrunk=0` is printed for a rename and a missing file, so the label does not name the actual reason (the gate's `isfile` check short-circuits). The outcome is red; the read token is misleading.

## Finding 2 — the non-shrink floor is the round-45 base (30696), not the wave-1 tip (40843): BROKEN

The wave-1 integration appended dispositions to the ledger: `git diff --stat eb874bc 96379ae -- corpus/knowledge` shows the ledger at +20 lines, and `wc -c` gives 30696 at `eb874bc`/`04af9bc` and 40843 at `HEAD`. The gate's floor (`EXEMPT_BASE_SIZE`) stays at 30696, so the appended dispositions can be removed silently.

Command: fixture = era export + `git show HEAD:corpus/knowledge/considerthese-proposals-ledger.md` truncated with `head -c N`:
```
N=31000  -> gate G6 pass=1 read=knowledge=65 entries=65 nested-md=65 base-intact=1 entry-bytes-ok=1 ; c2-gate fixed=7/7 exit=0
N=30696  -> gate G6 pass=1 read=knowledge=65 entries=65 nested-md=65 base-intact=1 entry-bytes-ok=1 ; c2-gate fixed=7/7 exit=0
N=30695  -> gate G6 pass=0 read=symlinks=0 exempt-entries-not-shrunk=0 ; c2-gate fixed=6/7 exit=1
```
Counterexample: truncating the tip ledger (40843 bytes) to 31000 bytes removes 9843 bytes of wave-1 dispositions and keeps the tree at 7/7 (see the N=31000 line above). The "bytes may grow never shrink" invariant is enforced only against the round-45 size (30696), so it does not protect the wave-1 appends that the exemption was added to protect.

Suggested direction (not applied; the lane's owner decides): anchor the floor to the tip size, or pin the ledger's prefix. Verified: `cmp <(git show eb874bc:corpus/knowledge/considerthese-proposals-ledger.md) <(git show HEAD:corpus/knowledge/considerthese-proposals-ledger.md | head -c 30696)` reports identical, so the wave-1 change is a pure append and a 30696-byte prefix pin would hold at the tip.

## Finding 3 — ledger content is not pinned; a same-name, grown rewrite reads green: BROKEN (by the stated design, but the design is weaker than the claim)

Command outputs:
```
mut-era-prefix-byte-flipped-plus-1-byte (byte 100 XOR 1, then one '\n' appended)
  -> gate G6 pass=1 read=knowledge=65 entries=65 nested-md=65 base-intact=1 entry-bytes-ok=1 ; c2-gate fixed=7/7 exit=0
mut-replaced-by-31000-byte-junk (1300 x 'junk line of filler text')
  -> gate G6 pass=1 read=knowledge=65 entries=65 nested-md=65 base-intact=1 entry-bytes-ok=1 ; c2-gate fixed=7/7 exit=0
```
So G6 proves the name and a size floor, not the round-45 history. The named mutants (shrunk, stubbed, swapped-name) are all red, but a rewrite that keeps the name and is at least 30696 bytes passes.

## Finding 4 — name pin is set-level, not name-to-bytes: swapped names of two exempt entries read green

```
mut-swap-names-claim-gates-and-claim-package -> gate G6 pass=1 read=knowledge=65 entries=65 nested-md=65 base-intact=1 entry-bytes-ok=1 ; c2-gate fixed=7/7 exit=0
```
The names set is unchanged, and both files are in the exempt set (content unpinned), so the swap is invisible. Same exemption mechanism (C1 entries); the ledger-specific swap (finding 1) is red only because of the size floor.

## Finding 5 — floors for the other two exempt entries are stale (6742 / 5169 vs base 15372 / 12319)

`git show 04af9bc:corpus/knowledge/claim-gates.md | wc -c` = 15372; `claim-package-contract.md` = 12319. `EXEMPT_BASE_SIZE` says 6742 and 5169. Fixture test:
```
mut-claim-gates-shrunk-to-6742-floor   (head -c 6742)  -> gate G6 pass=1 ... base-intact=1 ; c2-gate fixed=7/7 exit=0
mut-claim-package-shrunk-to-5169-floor (head -c 5169)  -> gate G6 pass=1 ... base-intact=1 ; c2-gate fixed=7/7 exit=0
```
A 56% (claim-gates 15372 -> 6742) and a 58% (claim-package-contract 12319 -> 5169) truncation of the two entries reads green. The floors do not match the sizes at the base commit `04af9bc` (15372 and 12319).

## Finding 6 — the era export: v1.2 bytes read 7/7 (holds) and v1.3 reads 7/7 on the same export

Command: `python3 era/corpus/instruments/r46-c2-gate.py --root era` (the `eb874bc` v1.2 bytes, blob sha256 `647bd5b7...`):
```
gate G1 pass=1 read=rows=28 admitted=28 entry=corpus/knowledge/github-private-vulnerability-reporting.md
gate G2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 full=4/4 anchored=1 table-rows=8 xrefs=4/4
gate G3 pass=1 read=row-S073=ok
gate G4 pass=1 read=recheck-rc=0 quotes-ok=8 frozen-cores-missing=0
gate G5 pass=1 read=spans=27 located=27 failed=0 uncited=0 cores=5/5
gate G6 pass=1 read=knowledge=65 entries=65 nested-md=65 base-intact=1 entry-bytes-ok=1
gate G7 pass=1 read=census-rc=0 ok-line=1
c2-gate fixed=7/7 exit=0
```
v1.3 bytes on the same export: identical 7/7 (`c2-gate fixed=7/7 exit=0`), matching E3's claim.

## Finding 7 — the selftest does not test the ledger

`corpus/instruments/r46-counters-selftest-c2.py` lines 67-68 only add `LEDGER` to `EXEMPT_ENTRIES` (so the byte-pin mutants never target the ledger). `grep -n -i ledger` finds no shrink, stub or swap case. The ledger's non-shrink is therefore covered only by the mutants above, not by the selftest.

## Limitations

- G7 calls the live `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` (outside the lane, not snapshotted). It read `census-rc=0 ok-line=1` on every run here; a change to that file would move G7 without any lane change.
- All G6 runs used the `era` export and the `tip` export (which is not in the lane's working tree; the working tree has many uncommitted `.ufo` changes, which I did not touch). G6 reads only `corpus/knowledge` and `corpus/README.md`/`SOURCES.md` via G1, so the uncommitted `.ufo` state does not enter these results.
- I did not re-run the attempt-1 counter selftests or the f29 gate; this item is limited to the ledger exemption.
- "Shrunk" is ambiguous in the item. I tested both readings: below the pinned floor (red) and below the wave-1 tip size but above the floor (green, finding 2).
- Fixtures were built by file copy and `head -c`/`printf`; no fixture was committed or written into the lane.
- Install/update record: none (no tools installed).

## Restoration / scratch

Scratch `/fast/scratch/hyaku/kasegi-r46/R46bW2MutPinAmend/` (exports, mutants, copies of the gate) removed before yield. No file in the lane, git, index, or fleet root was modified. One stray `/tmp/x` (30695 bytes, from a shell mistake) was created and removed immediately.
