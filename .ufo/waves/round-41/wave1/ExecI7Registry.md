# ExecI7Registry — round-41 I7 registry-row limb + D6 repair block

- Seat `ExecI7Registry` (executor, leaf). Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`
  — **read-only to this seat**: no lane file edited, no git/jj mutation (`git status --short` shows only
  untracked `.ufo/waves/round-41/` build files; `SKILL.md` sha256 `ad20fc3d…457c1` unchanged before and
  after every run). Fleet root and `~/Projects/*` never written.
- Axes: `depth:verifiability`, `coverage`. Milestone: round-41 build wave 1 (fresh-start). Item: the I7
  registry limb, its three required proofs, and the D6 repair bytes.
- Status: **delivered** — 3 deliverables + this receipt, all evidence re-run from the delivered bytes.
- Disk guard at start (`bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status`): `/tmp 3%
  125.1G free`, `/var/tmp 35% 589.5G`, `/fast/scratch/hyaku 24% 610.8G` — green (`exit=0`). No heavy pass
  was started before the guard read green.
- Scratch: `/fast/scratch/hyaku/kasegi-r41/ExecI7Registry/`, removed before yield (§6).
- Tools: GNU awk 5.4.1, GNU bash 5.3.20, coreutils, python3 (stdlib only). **No install or upgrade was
  needed**, so nothing is recorded in the install ledger.

## 1. Deliverables

| file | lines | bytes | sha256 |
|---|---:|---:|---|
| `.ufo/waves/round-41/wave1/ExecI7Registry.check.sh` | 135 | 6,206 | `60b963401d2535b0989abc686dfb5e9a73f888f14ba36c90632d6fa2c2064f6d` |
| `.ufo/waves/round-41/wave1/ExecI7Registry.skill-fix.txt` | 4 | 968 | `37d2b49d31d9235a4a9b9a35ca6105a6507bd63944c4ba1fc808c05b5eff70a6` |
| `.ufo/waves/round-41/wave1/ExecI7Registry.transcript.txt` | 229 | 24,934 | `4aaf7db685235e6eba7052aa4c58684ab62949a321d08e20a5a7e076cafa9454` |

Measured:

```
$ cd .ufo/waves/round-41/wave1 && for f in ExecI7Registry.check.sh \
      ExecI7Registry.skill-fix.txt ExecI7Registry.transcript.txt; do
    printf '%-34s lines=%-5s bytes=%-7s sha256=%s\n' "$f" \
      "$(wc -l < $f)" "$(stat -c%s $f)" "$(sha256sum $f | cut -d' ' -f1)"; done
ExecI7Registry.check.sh            lines=135  bytes=6206   sha256=60b963401d2535b0989abc686dfb5e9a73f888f14ba36c90632d6fa2c2064f6d
ExecI7Registry.skill-fix.txt       lines=4    bytes=968    sha256=37d2b49d31d9235a4a9b9a35ca6105a6507bd63944c4ba1fc808c05b5eff70a6
ExecI7Registry.transcript.txt      lines=229  bytes=24934  sha256=4aaf7db685235e6eba7052aa4c58684ab62949a321d08e20a5a7e076cafa9454
```

`ExecI7Registry.check.sh` is the **sourceable limb**: it defines one function and runs nothing when
sourced. `ExecI7Registry.skill-fix.txt` is the **D6 repair block** and contains only landable bytes.
`ExecI7Registry.transcript.txt` holds the proof transcripts.

## 2. The I7 limb (deliverable 1)

`i7_registry_row_check <skill_md_path> <instrument_basename>` — reads the given file, prints ONE payload
line, exit 0 iff a well-formed registry row exists.

```
registry=<0|1>,basename=<b>,candidates=<n>,valid=<n>,line=<n|0>,mentions=<m>[,reason=<why>]
```

A candidate row must satisfy **all five** clauses:

1. it is a markdown table line (0-3 leading spaces then a pipe);
2. it has ≥ 8 pipe-separated fields (`awk -F` field count ≥ 8);
3. its **FIRST cell** (`awk -F` field 2, trimmed) equals the basename **exactly** — a mention elsewhere in
   the row does not qualify (round-40 **T13**);
4. the immediately preceding line is a table row or a separator, **never a blank line** — a blank line
   ends a markdown table, so a row after one renders outside its header (round-40 **D6**, the live
   breakage at `SKILL.md` L1119-L1122: header L1119, separator L1120, blank L1121, row L1122);
5. it lies inside a **contiguous** table whose header row carries a `name` cell, whose next line is a
   delimiter row, and whose data rows sit below that delimiter.

Clause 5 anchors on the **run start**, not on the nearest `name`-looking line: in markdown a table is
exactly a run of `|`-lines whose *first* line is the header and whose *second* is the delimiter. Anchoring
on the nearest header-looking line instead is what lets a stray `| name | … |` data row masquerade as a
header — the run-start rule is the one that matches the renderer.

`candidates` counts rows whose field 2 is exactly the basename; `valid` counts those also passing 4-5;
`mentions` counts every line that *names* the basename but is not a valid row (the T13 class). Every
failing clause of a candidate is reported, not just the first, so the payload names exactly what is broken.

**`registry=1` means "at least one well-formed row exists", not "no malformed row exists".** `SKILL.md` is
append-only (round-41 I12), so a repaired table is *appended* and the malformed predecessor row is still
present — the L1 reads the malformed-row count from `candidates` vs `valid`, not from `registry`.

### The three required proofs (transcript §1, over scratch `SKILL.md` copies)

| proof | fixture | result |
|---|---|---|
| **T13 mention-only rejected** | `\| density.py notes (see r41-closure.sh for the gate that pins it) \| doc \| n/a \| …` | `registry=0 … candidates=0,mentions=1,reason=no-candidate-row` → exit 1 |
| **honest row passes** | header + delimiter + `\| r41-closure.sh \| gate \| … \|` | `registry=1 … candidates=1,valid=1,line=5` → exit 0 |
| **row after a blank line rejected** (live D6) | live `SKILL.md` L1119-1122 | `registry=0 … reason=L1122:preceding-line-not-a-table-row+header-row-has-no-name-cell` → exit 1 |

The prose-only variant of T13 (`r41-closure.sh is great …`, no table row at all) is rejected too, with
`mentions=1`. The live file's *well-formed* neighbour row is the live control: `r39-closure.sh` →
`registry=1,valid=1,line=1115` → exit 0, so the limb is not simply red on the live file.

### Every clause is load-bearing (transcript §4)

13 mutants, each collapsing exactly one clause of the **shipped** awk program (extracted from the
delivered file, not re-implemented), compared on **full payload** across 9 fixtures. **All 13 killed; 0
survivors.** Collapsing the field-2 exact match turns the mention-only fixture green (M1); collapsing the
field-count floor turns the truncated-row fixture green (M2); collapsing the preceding-line check drops
`preceding-line-not-a-table-row` from the D6 reason (M3); collapsing the header-name check turns the
no-`name`-header fixture green (M4, M8); collapsing the delimiter check turns the no-delimiter fixture
green (M5, M11); collapsing the below-delimiter check turns the delimiter-row fixture green (M6);
collapsing the table-line check turns the 4-space-indented fixture green (M7); and the verdict rule,
mentions accounting and run-start walk all change their fixtures when collapsed (M9, M10, M12, M13).

Two mutants were added after the first battery showed survivors, rather than leaving the clauses
unproven: **F9** (a fixture whose delimiter row's field 2 *is* the basename) makes the below-delimiter
clause killable, and the comparison was corrected to use the full payload — the earlier version stripped
the basename with an over-matching glob that masked real payload differences and misreported M3/M5/M11.

### Sourceability (transcript §5)

Sourcing `ExecI7Registry.check.sh` defines `i7_registry_row_check`, prints nothing, and leaves the
lane's `SKILL.md` byte-identical (`sha256` equal before/after). The function then works normally. A
missing file and a missing argument both exit **2** (fail-closed, distinct from the exit-1 verdict).

## 3. The D6 repair block (deliverable 2)

`ExecI7Registry.skill-fix.txt` = 4 lines: a **leading blank line**, then `SKILL.md` L1119 (header),
L1120 (separator) and **L1122 (the `r40-closure.sh` row) copied byte-exact**. The row bytes are
verbatim — the committed unescaped `|` inside backticked spans (`` `closed=0|1` ``) is preserved, because
verbatim means verbatim.

Byte-identity against the committed file:

```
$ awk 'NR==1122' SKILL.md | sha256sum
20402c77e39edc8b337852ff69e83ca39b19b5b6da7f5484522afb978e503164  -
$ tail -1 ExecI7Registry.skill-fix.txt | sha256sum
20402c77e39edc8b337852ff69e83ca39b19b5b6da7f5484522afb978e503164  -
$ awk 'NR==1119||NR==1120' SKILL.md | sha256sum
ac5cee380f96e9ab3ffdeb97d3388f6933b07bc97c747e5bcfe5571ae33f2c75  -
$ sed -n '2,3p' ExecI7Registry.skill-fix.txt | sha256sum
ac5cee380f96e9ab3ffdeb97d3388f6933b07bc97c747e5bcfe5571ae33f2c75  -
```

**Independent corroboration:** the sibling seat `RevD4D5D6` (reviewer) derived the same D6 block
separately, and the two files are byte-identical —
`cmp ExecI7Registry.skill-fix.txt RevD4D5D6.skill-table-fix.txt` → silent, both
sha256 `37d2b49d31d9235a4a9b9a35ca6105a6507bd63944c4ba1fc808c05b5eff70a6`. Two independent derivations
agreeing byte-for-byte is the strongest available evidence that the repair is right; **the L1 should land
one copy, not both.**

### Landing proofs (transcript §2)

| landing | result |
|---|---|
| **L1** repair appended at EOF (the append-only landing) | `registry=1 … candidates=2,valid=1,line=1126` → exit 0 |
| **L2** repair inlined (blank at L1121 removed, row re-attached) | `registry=1 … candidates=1,valid=1,line=1121` → exit 0 |
| **L3/L5** the block alone, no surrounding context | `registry=1 … valid=1,line=4` → exit 0 |
| **L4** repair appended **without** the leading blank line | `registry=0 … reason=L1122:…+…;L1125:header-row-has-no-name-cell` → exit 1 |

**L4 is the reason the leading blank line is in the deliverable.** Without it the appended header merges
into the orphaned row's broken run, so the new row inherits the breakage and *both* rows stay red. The
blank line is load-bearing, not decoration. The L1 should therefore append the file **verbatim at EOF**
(leading blank included) and must not strip it.

The block is self-contained and append-only: the committed orphan at L1122 is left untouched (no rewrite,
no deletion), matching the append-only rule.

## 4. Landing notes for the L1

- `ExecI7Registry.skill-fix.txt` → append **verbatim** at EOF of `SKILL.md` (the file ends with `\n`; the
  deliverable's leading blank line supplies the table separation). Do **not** append it twice — the
  sibling `RevD4D5D6.skill-table-fix.txt` is byte-identical (see §3); land one.
- `ExecI7Registry.check.sh` → sourceable limb. To use it inside the round-41 suite `r41-closure.sh`, `.`
  the file (or paste the function) and call
  `i7_registry_row_check "$tree/SKILL.md" <basename>`; the payload's `registry=1` is the green condition
  and `candidates` vs `valid` exposes any still-malformed row. The function reads only the file it is
  given, writes nothing, and touches no git state.
- The limb is basename-parameterised: pass `r41-closure.sh` to gate the new suite's own registry row, or
  `r40-closure.sh` to gate the D6 repair. Live measurement at the receipt time:
  `r39-closure.sh` → `registry=1,valid=1,line=1115`; `r40-closure.sh` → `registry=0` (D6 unlanded);
  `r41-closure.sh` → `registry=0,reason=no-candidate-row` (no row yet — expected before the L1 lands it).

## 5. Evidence retained (exact commands and outputs)

- `ExecI7Registry.transcript.txt` (229 lines) — §1 the three required proofs over scratch `SKILL.md`
  copies; §2 the four landing proofs; §3 the live-file edge-case sweep (every basename the live registry
  names, plus no-`name`-header, no-delimiter, backticked-name, old-broken-plus-appended-good,
  idempotence, and a before/after `SKILL.md` sha256 showing the lane file was never written); §4 the
  13-mutant battery; §5 sourceability.
- Live lane state was read only. `git status --short` shows **no** tracked-file modification; `SKILL.md`
  sha256 is `ad20fc3d371302301b49088ae41c0a227cf6067ea0c6c8078f2f000d1ca457c1` before and after.
- CRLF and unescaped-pipe rows were checked separately (both accepted correctly).

## 6. Risks and blockers

- **Risk (medium, for the L1):** the D6 repair block must be appended **with** its leading blank line and
  **once**. Appending without it leaves the table broken (§2 L4); appending both my copy and the sibling's
  byte-identical copy would duplicate the row block. Both are called out in §3/§4.
- **Risk (low):** the limb gates on a *contiguous* table with a `name` header. It does not check that the
  row is under a specific `## Round-NN Gates & probes registry addition` heading, nor that `owner` is
  populated — the item named five clauses and this implements exactly those. A registry row that satisfies
  all five but sits under an unrelated heading would still pass; tightening that is the L1's call.
- **Risk (low):** `registry=1` is existential. If the L1 wants "no malformed row anywhere", read
  `candidates` vs `valid` (the D6 orphan shows up as `candidates=2,valid=1` after the append) rather than
  the `registry` bit alone.
- **Blockers:** none. The item is fully delivered and every acceptance claim is re-run from the delivered
  bytes.
- **Not claimed:** this seat does not verify that `r41-closure.sh` (the round-41 suite) itself exists or
  passes — that is another seat's instrument. This seat delivers the I7 limb and the D6 repair only.

## 7. Cleanup

Scratch `/fast/scratch/hyaku/kasegi-r41/ExecI7Registry/` is removed before yield (§6 of the seat rules:
no seat scratch dir may survive). Deliverables and this receipt live in the lane's wave directory.
