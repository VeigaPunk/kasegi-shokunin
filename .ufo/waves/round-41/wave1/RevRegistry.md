# RevRegistry — round-41 wave-1 receipt

Seat: RevRegistry (reviewer, leaf). Item: review the SKILL.md registry repair plan (D6 + the r41 row).
Lane: /home/vgpnk/Projects/shokunin/kasegi-shokunin. Scratch: /fast/scratch/hyaku/kasegi-r41/RevRegistry (removed at yield).
Tools: system bash/coreutils/git only (no installs needed; pacman untouched per operator pause).

## Verdict

**PASS with two flags for the L1** — (i) no wave-1 seat authors the r41 registry row bytes; the L1
must author them at integration to the contract below. (ii) The appended r41 block MUST be separated
from the D6-fix block by a blank line (and should carry the round-41 heading); appending it directly
after the fix block fuses the new header into the fix table as a data row.

## 1. The repaired table renders (blank-line rule) — VERIFIED

Live state (HEAD b3b08b2 == working tree, `git status` clean; sha256
`ad20fc3d371302301b49088ae41c0a227cf6067ea0c6c8078f2f000d1ca457c1`, 1122 lines, matches the
SHONEN box-1 claim; `git diff --numstat 5b29ea1439450b712581edf5f0f0bf98dfb262ab b3b08b2 -- SKILL.md`
is empty — no base line touched through the spec head):

- `SKILL.md:1119` header, `:1120` separator `|---|---|---|---|---|---|---|---|`, `:1121` **blank**,
  `:1122` the `r40-closure.sh` row. A blank line ends a Markdown table; the row renders outside its
  header (D6 as routed).

Operative check (I7 semantics, modeled on ExecI7Registry's spec: first cell == basename, >=8 fields,
preceding line a row/separator never blank, contiguous table whose header contains `name`), run from
scratch over the live file:

```
row line=1122 fields=13 : | r40-closure.sh | gate | `bash corpus/instruments/r40-closure.sh --ex
REJECT preceding blank line (D6 class)
REJECT no row with first cell == r41-closure.sh
```

Repair deliverable actually landed: `wave1/RevD4D5D6.skill-table-fix.txt` (4 lines, sha256
`37d2b49d31d9235a4a9b9a35ca6105a6507bd63944c4ba1fc808c05b5eff70a6`) = leading blank, the exact header
`| name | type | entry command | verdict map | self-test | pinned-value path | write scope | owner |`,
the 8-column separator, then the r40 row. I extracted `SKILL.md:1122` to scratch and
`cmp` is silent — **row bytes byte-identical** (my extraction sha256 `20402c77e39edc8b337852ff69e83ca39b19b5b6da7f5484522afb978e503164`).
The leading blank is required: it separates the new block from the previous tail so the header opens
a fresh table. (ExecI7Registry's `skill-fix.txt` is spec'd to the same shape but was NOT yet landed at
review time; recommend the L1 `cmp` the two fix blocks and land one.)

Simulated full landing in scratch (base SKILL.md + the landed fix + a round-41 heading + the r41 row,
blank-separated blocks, `skill-landB.md`):

```
row line=1122 fields=13 ... REJECT preceding blank line (D6 class)   <- historical orphan stays broken, expected
row line=1126 fields=13 ... PASS contiguous table, header contains name: | name | type | entry command | ...
row line=1132 fields=14 ... PASS contiguous table, header contains name: | name | type | entry command | ...
```

## 2. r41 row carries the 8 header columns — VERIFIED (contract stated; bytes are L1-authored)

Header columns: `name | type | entry command | verdict map | self-test | pinned-value path | write scope | owner`.
Drafted a conformant r41 row in scratch per the frozen C1 predicate and the r39/r40 row pattern; split
on unescaped pipes only it yields **exactly 8 logical cells** (the r40 verbatim row yields 11 — see
finding F-obs-1). Contract the L1's row must meet:

1. logical cells == 8 — every alternation pipe inside a cell escaped `\|` (the r36 rows set the
   precedent: `gate\|probe`, `exit=0\|1`); bare `0|1`-style pipes split cells (the r40 row's defect);
2. cell 1 = `r41-closure.sh` (exact, for the I7 first-cell awk limb);
3. cell 2 = `gate`;
4. cell 3 = entry command `bash corpus/instruments/r41-closure.sh --export-ref <hash> ...`
   (export-mode only; plain run refuses exit 2);
5. cell 4 = verdict map: one `` `I<n> payload=… closed=0\|1` `` line per check I1–I12, then
   `` `closed=K/12 exit=0\|1` ``; exit 0 only for K=12;
6. cell 5 = self-test: `--selftest --export-ref <hash>` → twelve graded
   `selftest case=I<i> … positive=pass … verdict=pass` lines + `selftest cases=12 failures=0`;
7. cell 6 = pinned-value path (see §3);
8. cell 7 = `read-only (export and receipt-out in scratch)`; cell 8 = `kasegi (round 41; I1–I12)`.

## 3. Pinned-value path names the r41 receipt — VERIFIED as plan requirement

The judged-head rule names the round-41 receipt `.ufo/waves/round-41/final-gates/all-gates.txt` (the
lane tip Y adds only that file). My draft's pinned-value cell reads:

```
base `5b29ea1439450b712581edf5f0f0bf98dfb262ab` and r40 judged head
`c7aea5ef97902f38289cbdc1cf267068876a62dd` → `closed<12/12 exit=1`; r41 receipt
`.ufo/waves/round-41/final-gates/all-gates.txt` at Y → `closed=12/12 exit=0`
```

(`grep -c "ufo/waves/round-41/final-gates/all-gates.txt" r41-row-draft.txt` → 1.) The L1-authored row
must name this path — it is the pinned-value anchor the I2/I8 limbs bind.

## 4. Append-only — VERIFIED (current + simulated)

- `git diff --numstat 5b29ea1439450b712581edf5f0f0bf98dfb262ab b3b08b2 -- SKILL.md` → empty (0 lines);
  working tree == HEAD; file sha256 equals the base-era hash quoted above.
- Simulated landing diff vs base: `1122a1123,1132` — 10 added lines, **0 removed/modified**
  (`diff` `^<` count = 0). The repair is a pure EOF append; the broken round-40 block stays in place
  as history (the spotcheck's prescribed fix: "an appended, correctly formed row block", not a rewrite).

## Findings

- **F-gap-1 (plan gap, L1 action):** no wave-1 seat is tasked with the r41 registry row bytes
  (checked all 60 wave1-spec items; only ExecI7Registry and RevD4D5D6 author the r40-row fix). The L1
  authors the row at integration to the §2 contract. Severity: high if missed (I7 has no r41 row to
  find); cheap to land.
- **F-haz-1 (landing hazard):** if the r41 block is appended directly after the D6-fix block with no
  blank line between the fix's r40 row and the r41 header, the two fuse into one table and the second
  `| name | …` header renders as a junk data row (demonstrated on `skill-landA.md`; the I7-style check
  still PASSes — contiguity is satisfied — so the line-anchored limb alone cannot catch this).
  Require: blank line before the r41 block header, and per every prior round's convention a
  `## Round-41 Gates & probes registry addition (appended 2026-10-27)` heading.
- **F-obs-1 (no action, for the record):** the verbatim r40 row has 11 logical cells — three unescaped
  pipes inside backticked spans (`` `closed=0|1` ``, `` `exit=0|1` ``, `` `verdict=pass|fail` ``). The
  spotcheck mandates verbatim copy, and the I7 limb is `>=8 fields` (row = 13 awk fields), so this
  passes; renderers will truncate the visual tail. Do NOT "fix" the pipes — that would violate
  append-only/verbatim.
- **F-obs-2 (out of item scope, recorded):** live `claims.json` C1 predicate/kill_rule still read
  "the seven committed CritKillRule escape states" while its own correction fields and
  `wave1/CORRECTIONS-L1.md` mandate eight (F1–F8, `escapes=8 red=8`). The correction note is declared
  authoritative; flagging so no seat treats the stale predicate literal as the target.

## Verification gaps

- No Markdown renderer on host (no pandoc, no python-markdown); rendering was verified with the
  operative line-anchored rule (the exact I7 limb semantics), not a renderer dump.
- ExecI7Registry.skill-fix.txt not yet landed at review time; its spec'd bytes equal the landed
  RevD4D5D6 block in shape (header + separator + L1122 verbatim). L1 should cmp and dedupe.

No deliverable file (receipt-only item). Reviewed artifacts: SKILL.md tail L1104-1122,
wave1/RevD4D5D6.skill-table-fix.txt (sha256 above), wave1/CORRECTIONS-L1.md,
wave1/ScribeShonenLog.shonen-append.txt box 1, .ufo/waves/round-41/claims.json (40-char base
`5b29ea1439450b712581edf5f0f0bf98dfb262ab` confirmed resolvable; the 38-char literal appears only in
the correction record as the documented typo).
