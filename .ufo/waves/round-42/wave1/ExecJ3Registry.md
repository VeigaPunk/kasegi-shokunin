# ExecJ3Registry — round-42 C1 J3 (family F-TABLE): SKILL.md registry integrity

Seat: **ExecJ3Registry** (executor, leaf). Lane `kasegi-shokunin`. Base
`5053a7f46de35784cff4b56756906e9014a38276`; lane HEAD at transcript time
`514ff62d61ee9bc717a20a02a22c65ec0c5124ed` (claims erratum 3). `SKILL.md` is
byte-identical at base, at HEAD and at the round-41 judged head
`1f7464612ac4c44e39886b82e812610d3c039b13`: sha256
`f8e7a5d3be74699329162635b26731e0ce156483dc17bd29a3323eef15413e00`, 1129 lines.
No tool installed, no network fetch, nothing written outside scratch and the
four wave-1 artifacts below. Scratch `/fast/scratch/hyaku/kasegi-r42/ExecJ3Registry`
removed before yield.

## Deliverables (all under `.ufo/waves/round-42/wave1/`)

| file | lines | sha256 |
|---|---|---|
| `ExecJ3Registry.sh` (sourceable limb: `check_j3`, `j3_line`, `j3_replay`) | 541 | `8418dc6d61de37e156fb5f63ab1d55601da3b90918add032af205b03a2b3520b` |
| `ExecJ3Registry.skill-fix.txt` (landable block, **replaces SKILL.md L977–L1129**) | 151 | `22785bde5f6abdd51292dc6dabb6afb6bfce3fbfc583b17688d20727deb0f171` |
| `ExecJ3Registry.transcript.txt` (teed run: red at HEAD/base/r41-head, green on the fixed bytes, replay, coupling probes) | 203 | `812f52050a7fd88bcff49b7446981b731e3ce5a1635ea5af164714101bc24ce2` |

Landing the block alone yields a 1127-line `SKILL.md` with sha256
`3e90d62057c2e62ce67f443e73d6a8f68e8e0c94d468a8eaade7a0c4121900a8` (measured, see
transcript §5).

## 1. D-r41-3 measured exactly (not from the route note)

`bash ExecJ3Registry.sh --detail <export of HEAD>`, verbatim:

```
defect: badcells L981 cells=9 want=8
defect: badcells L982 cells=9 want=8
defect: badcells L1041 cells=9 want=8
defect: badcells L1054 cells=9 want=8
defect: badcells L1055 cells=9 want=8
defect: split L1119 registry table has no data row
defect: orphan L1122 r40-closure.sh is not inside a registry table
defect: dup L0 r40-closure.sh rows=2
tables=9,rows=18,split=1,orphan=1,badcells=5,leadws=0,indent=0,dup=1,missing=0,unknown=0,declared=1,own=r42-closure.sh,read=ok
```

- **Split table**: L1120 is the Round-40 separator, L1121 the blank line, L1122 the
  `r40-closure.sh` row. In a CommonMark table a blank line ends the table, so the row
  renders outside its header (round-40 verifier D6).
- **Duplicate identity**: `r40-closure.sh` at L1122 (Round-40 block) and L1128
  (Round-41 block). The two rows are **not** byte-identical: L1122 is the garbled
  11-cell variant (bare `closed=0|1`, `exit=0|1`, `verdict=pass|fail` inside cells;
  write-scope cell mangled as ``scratch/` --receipt-out` only``), L1128 is the
  sanitised 8-cell variant (`closed=0-or-1`, `verdict=pass-or-fail`, clean
  write scope). Both carry the same instrument pin (`bdbd18a3239c…`, 1734 lines), so
  moving the sanitised text into the Round-40 block loses no provenance — it is the
  round-41 author's own correction of the same row (matches RevRegistry's reference fix).
- **Five legacy bare pipes** (same defect class, not named by D-r41-3): L981, L982,
  L1041, L1054, L1055 carry `gate|probe` unescaped → 9 cells in an 8-column table.
  Every registry row that carries a two-type cell from the round-31 block on already
  writes `gate\|probe` (L1064, L1077, L1097, L1098, L1110, L1111 — rows whose type is
  a single `gate` have no pipe to escape), so escaping is the file's own convention.
- **Declared pair** (erratum E3, not a defect): `r36-closure.sh` at L1111/L1113, two
  Round-36 rows with distinct verdict maps (the second is the D5 correction appended
  in round 37); `anchorcheck.py` at L982/L1041 is documented history but is not an
  `r*-closure.sh`, so the scoped limb never sees it.

## 2. The fix and how to land it

`ExecJ3Registry.skill-fix.txt` is the corrected bytes of **SKILL.md lines 977–1129**
(from the `## Gates & probes registry` heading to EOF). Landing recipe (byte-exact):

```
head -976 SKILL.md > SKILL.md.new
cat ExecJ3Registry.skill-fix.txt >> SKILL.md.new
mv SKILL.md.new SKILL.md        # expect 1127 lines, sha256 3e90d620…4121900a8
```

The block **modifies six lines and deletes two** (transcript §6; `diff -u` shows
four hunks):

1. L981 `gate|probe` → `gate\|probe` (recheck-audit.py)
2. L982 `gate|probe` → `gate\|probe` (anchorcheck.py)
3. L1041 `gate|probe` → `gate\|probe` (anchorcheck.py, round-29 row)
4. L1054 `gate|probe` → `gate\|probe` (frontier-recheck-count.py)
5. L1055 `gate|probe` → `gate\|probe` (source-recheck.py)
6. L1122 (the garbled r40 row) → the sanitised L1128 text, now contiguous with its separator
7. **deleted:** L1121 (the blank line) and L1128 (the duplicate row)

**Why the five escapes are in scope.** Erratum E3 (committed `27e18d2`) rules that
"the contiguity limb … and the bare-pipe / leading-whitespace cell limbs apply to all
Gates-and-probes rows", while "legacy rows' escaped `\|` cells are ACCEPTED" and the
limb "rejects only unescaped pipes that change a row's cell count". A check that
honours that scope is red at Y on those five rows (they give 9 cells in an 8-column
table) unless they are escaped. RevRegistry F1.2 offered exactly the two branches
("escaped … or the check is scoped to blocks r36+") and required the choice to be
written into the replay limb; E3 picked "all rows", so the repair escapes them. I did
not scope the limb down to make it green: wave-2 seed item 86 ("attack both") is the
reason a scoped-out bare-pipe rule would be an in-family escape. Escaping preserves
the rendered cell content exactly (GFM renders `\|` as `|`) and fixes the table
column count that is broken today.

**Depth:density delta, disclosed.** `density.py` on `SKILL.md`: mean dens **237.1 →
234.0**, path citations **780 → 777** (29 blocks both sides). The only citation change
comes from deleting the duplicate row; the five escapes change no citation. This is
the consequence erratum E5 already discloses; `corpus/instruments/density.py` bytes
are untouched (J12's owned-axis guard).

**Ordering hazards for the L1 (read before landing).**
- Land this block **before** any other SKILL.md edit inside L977–1129. In particular
  `ConnCrossClaims` H3(b)'s J6 re-pin of `capture-binding-check.py` (the pin paragraph
  in the Round-33 block) must be applied **after** the block, or it will be reverted.
  The block reproduces every line it does not change byte-for-byte.
- The block deliberately contains **no `r42-closure.sh` registry row** (see §5). If
  you add one, add exactly one, inside the same region, and keep it pipe-clean.

## 3. `check_j3` — contract and scope decisions

Sourceable bash limb, house style of `ExecJ5Scan.sh` / `ExecJ12J13.sh`:

```
check_j3 TREE [REF]      # REF accepted and ignored (r41 run_check TREE REF dispatch)
  -> one payload line `k=v,k=v,...`, exit 0 closed / 1 red / (2 harness error)
j3_line TREE             # the same check composed as `J3 payload=… closed=<0|1>`
j3_replay TREE SANDBOX   # the REPLAY limb (12 graded cases)
```

Payload keys (all gating except `unknown`, `declared`, `own`, `read`):
`tables rows split orphan badcells leadws indent dup missing unknown declared own read`
— `split` (blank line between a separator and its rows; the D-r41-3 shape),
`orphan` (row naming a closure suite but outside a registry table; the
"moved outside"/"after a blank line" shapes), `badcells` (cell count ≠ the table
header's; cells are split on **unescaped** pipes only, so `\|` is accepted and a bare
pipe is rejected), `leadws` (first cell not exactly `| <name> |`), `indent` (row not at
column 0 — an indented row still counts for `dup`), `dup` (a `r*-closure.sh` basename
in more than one row, counted across **all** tables and orphan rows),
`missing` (an on-disk `corpus/instruments/r*-closure.sh` with no row).

Registry tables are selected by their header (`name`, `type`, `entry command`, 8
columns) — **not** "any `|` line after L977" — so the 4-column Frontier decision table,
the policy playbook, the `limb-mutation-check.py + limb-ledger.json` two-name first cell
(L1064) and pipe tables in prose never leak into the check (wave-2 seed item 88).
Fenced regions are skipped.

Two scope decisions, both forced by committed text and both printed in the payload:

1. **Declared pair** — erratum E3 scopes uniqueness to `r*-closure.sh` basenames
   "exclusive of those declared pairs". `J3_DECLARED_PAIRS` defaults to
   `r36-closure.sh`; the pair is exempt from `dup` **only** (both rows are still
   contiguity/cell/padding-checked). Transcript §11 shows the exemption is real:
   `J3_DECLARED_PAIRS=''` turns the same bytes RED with `dup=1`.
2. **Own instrument** — `missing` skips the suite-under-test basename
   (`J3_OWN`, default `r42-closure.sh`). The suite's own registry row is the
   integration's artifact (ConnCrossClaims H3: "Any r42 registry row goes inside the
   same replacement"), and the negative controls run on base / round-41 exports where
   the suite does not exist at all. It is still subject to every other limb, `dup`
   included. Transcript §10 shows both sides: `J3_OWN=''` on a tree that carries the
   suite file but no r42 row gives `missing=1` RED.

Statement of what J3 is **not** (documented in the limb header): it is a **shape**
check. It cannot judge whether a row's verdict-map prose is true (wave-2 seed item
84), and it does not police non-registry tables. The receipt makes no content claim.

## 4. Evidence (full transcript in `ExecJ3Registry.transcript.txt`)

| run | result |
|---|---|
| `--detail` on the HEAD export | RED: the 8 defect lines quoted in §1 |
| `--check` on the base export / r41 judged-head export | RED, identical payload (`split=1,orphan=1,badcells=5,dup=1`) |
| block applied to a scratch copy of the export | `--check` → `split=0,orphan=0,badcells=0,leadws=0,indent=0,dup=0,missing=0 … read=ok`, exit 0 |
| `--line` (both states) | `J3 payload=… closed=1` on the fix, `closed=0` on HEAD |
| `--self-test` (replay) on the fixed bytes | `selftest cases=12 failures=0`, exit 0 |
| pipe census | bare `gate|probe` 5 → 0; escaped `gate\|probe` 6 → 11 |
| no row lost | every on-disk closure suite still has ≥1 row (`r35-defect` 1, `r36` 2, `r37` 1, `r38` 1, `r39` 1, `r40` 1, `r41` 1, `r-defect` 1) |

Fail-closed checks run against the limb (not in the transcript, re-runnable):
`sourcing runs nothing` (a `source` prints only the wrapper's own echo); no arguments →
exit 2; missing `SKILL.md` → `read=fail,reason=no-skill-md` exit 1; missing
`corpus/instruments/` → `read=fail,reason=no-instruments` exit 1; nonexistent tree →
`read=fail,reason=no-tree` exit 1; `check_j3`'s payload carries no trailing newline, so
the suite's `$(...)` capture composes cleanly.

## 5. REPLAY limb — every committed F-TABLE defeat re-executed and rejected

`j3_replay TREE SANDBOX` materializes each defeat shape in its own directory under
SANDBOX (never inside TREE) and requires the **current** bytes' limb to reject it; the
unmutated positive must be accepted. A case that cannot be materialized counts as a
failure, so an absent defeat can never read as a repair.

| case | source | observed |
|---|---|---|
| positive | fixed bytes | accepted (`closed=1`) |
| m1 blank line directly before the suite row | MutSkillTablePipes probe 1 | rejected (`split=1,orphan=1`) |
| m2 bare pipe appended inside an entry command | MutSkillTablePipes probe 2 (r41 **survived**) | rejected (`badcells=1`) |
| m3 leading whitespace in the first cell | MutSkillTablePipes probe 3 (r41 **survived**) | rejected (`leadws=1`) |
| m4 suite row moved outside the contiguous table | MutSkillTablePipes probe 4 | rejected (`split=1,orphan=1`) |
| m5 duplicate row appended at EOF | D-r41-3 shape | rejected (`dup=1`) |
| m6 indented duplicate row | wave-2 seed 79 | rejected (`indent=1,dup=1`) |
| m7 blank line between header and separator | wave-2 seed 81 | rejected (`split=1,orphan=1`) |
| m8 row deleted | wave-2 seed 83 (missing direction) | rejected (`missing=1`) |
| m9 legacy bare pipe re-introduced | wave-2 seed 86 | rejected (`badcells=1`) |
| m10 duplicate row inside the same table | wave-2 seed 83 | rejected (`dup=1`) |
| m11 duplicate row in a **different** registry table | the exact D-r41-3 cross-table shape | rejected (`dup=1`) |

The two round-41 survivors (m2, m3) are the ones MutSkillTablePipes recorded as
`survived; coverage finding`; both are now rejected. The replay proves rejection on
the post-repair bytes, so it cannot be satisfied by the pre-repair state.

## 6. Integration notes for the L1

- **The r42 registry row.** Because `corpus/instruments/r42-closure.sh` will exist in
  the Y export, the seat spec's "exactly one registry row" would demand a row for it.
  I chose not to ship one in the block: if you author your own and mine were also
  present, J3 would be RED with `dup=1` — the exact defect this round repairs. The
  coupling is therefore explicit, not hidden: with the suite file present and no row,
  `J3_OWN=''` reads `missing=1` (transcript §10). A tested, pipe-clean, 8-cell row is
  printed in transcript §12; exactly one copy of it (or of an equivalent row) keeps
  `missing=0, dup=0`. Two copies read `dup=1` RED (transcript §12, second half).
- **J12 compatibility.** The repair deletes two SKILL.md lines and modifies six. Per
  erratum E5, J12 is scoped to `corpus/` deletions plus `density.py` byte-identity, so
  the retired r41 `skdel==0` clause must **not** be ported into J12 (J12's owner,
  `ExecJ12J13.sh`, already states this).
- **Suite wiring.** `check_j3 "$EXPORT" "$REF"` returns the bare payload (r41 harness
  convention: the suite prints `J3 payload=<payload> closed=<0|1>`); `j3_line "$EXPORT"`
  returns the composed line if your harness prefers it whole. The limb reads only
  `TREE/SKILL.md` plus a directory listing of `TREE/corpus/instruments/`.

## 7. Risks and open items

- **Landing scope.** The block is 151 lines because it must include the whole registry
  section (the five legacy escapes sit at 981–1055, far above the tail). Splice it
  first, then apply J6's re-pin and any r42 row. Applying it after those edits reverts
  them.
- **Declared-pair exemption.** If you prefer strict one-row-per-basename, the r36 pair
  must be merged first; today `J3_DECLARED_PAIRS=''` is RED by design (erratum E3
  declares the pair legitimate).
- **`unknown` is diagnostic only**, so a registry row naming a typo'd basename would
  not red J3 (`badcells`/`leadws` still apply). Stated rather than hidden.
- Nothing here is a blocker; no question is open for the L1.

## 8. Provenance

Commands are recorded verbatim in `ExecJ3Registry.transcript.txt` (each line starting
`$ ` was executed in that run). Read-only lane access only: `git rev-parse`,
`git cat-file blob`, `git archive <ref> | tar -x` into scratch; no mutating git/jj
command was run. No package/tool installation, no network fetch. Scratch
`/fast/scratch/hyaku/kasegi-r42/ExecJ3Registry` (exports, fixtures, sandbox) removed
before yield.
