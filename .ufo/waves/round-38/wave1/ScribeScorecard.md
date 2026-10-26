# ScribeScorecard — round-38 receipt

Seat `ScribeScorecard` (leaf scribe, lane `kasegi-shokunin`, round 38, attempt 1). Lane repo
`/home/vgpnk/Projects/shokunin/kasegi-shokunin`; base `a173b0c2b98c5ae39599fa9be76027fbbead0b9e`;
claims-freeze commit `9a10b02fe411bb8d9d71aed3b1d3a5949d50d16b`; frozen claims read from
`.ufo/waves/round-38/claims.json` (`frozen_at_utc` `2026-10-26T18:17:40Z`) and not edited.

Item: draft (a) the SCORECARD.md `Correction (round 38)` line and (b) the `## Round 38 result`
section, byte-exact.

## 1. Deliverables

| File | Bytes | Lines | sha256 |
|---|---:|---:|---|
| `.ufo/waves/round-38/wave1/ScribeScorecard.correction.md` | 375 | 1 | `e9f0c1e1658e0e36e8c942e49a18e0fdeef7ebf0464b3636d6bbcdc06d33425d` |
| `.ufo/waves/round-38/wave1/ScribeScorecard.section.md` | 3472 | 12 | `f09d58db2a1032c2731f02cad39851efad17974a0a3ca2bab856c8c1be05f564` |

Both files end with a newline; each copy in the wave dir was `cmp`-compared to the scratch draft
(`correction-cmp-identical`, `section-cmp-identical`) before the scratch tree was removed.

Read-only base surface: `SCORECARD.md` at lane HEAD `700153593eb586c70a6499c8ca225ee4d673bc9b` —
1509 lines, sha256 `1047ba2bcd02b462b79fbb1b14098eb7ee49d6af07b6a9ca47e908ca0ce470ee`. The base
file's last block is `## Round 37 result` (heading at line 1496), ending with the labelled line
`Final lane commit: f3246559bed2fd085dde860e00247ce394f02bad (round-37 wave-evidence ancestor; …)`.

**Landing order (load-bearing, not cosmetic).** Append in this order at EOF: blank line, the
correction line, blank line, the `## Round 38 result` heading and its section. The correction line
must sit *outside* the round-38 section (i.e. between the round-37 block and the round-38 heading).
Two frozen checks force this: G5's rule that the `^## Round 38` section contains zero lines with
`Final lane commit:` cannot hold if the correction line (which quotes the r37 label) is inside the
section, and G2's per-line regex `(final (lane )?(head|commit)|judged head)[^|]*[0-9a-f]{7,40}`
would match it there. Appended last instead of before the heading, the correction line falls inside
the section (the section runs to the next `^## ` heading or EOF) and both checks go red.

Composition exercised for validation (scratch only): base `SCORECARD.md` + blank + correction line +
blank + section = 1524 lines, round-38 section at composed lines 1513–1524.

## 2. What the deliverables contain

(a) One line beginning `Correction (round 38): ` that quotes the round-37 section's
`Final lane commit: f3246559…` line, states it names a wave-evidence anchor ancestor, not a final
head, gives the read form `Anchor ancestor (r37 wave evidence): f3246559bed2fd085dde860e00247ce394f02bad`,
names the round-37 judged head `2387dcf6ccfefcfb703783387b9aade8fc82abfa` and its tip
`83975acc83df4bd8d5eaf463182ae615f2b64546`, and cites `(verifier §5 D-D)`.

(b) `## Round 38 result` in the round-37 section's shape: a five-column axes table with three rows
(`depth:verifiability` 4 → 4 (held), `coverage` 7 → 7 (held), `depth:density` 9 → 9, non-target
guard), the exact line `Measured before: freeze 9a10b02fe411bb8d9d71aed3b1d3a5949d50d16b` (paired
with the three frozen before-files), the exact line
`judged head: export-ref of .ufo/waves/round-38/final-gates/all-gates.txt`, and a `Measured after:`
line carrying every counting command from `claims.json` C1 and C2 with the frozen expected outputs.
No hash is labelled final/judged head; the section names J only by reference to the receipt file.

`[L1-MEASURE]` appears exactly 3 times — the three after-cells (one per axis) the L1 replaces with
measured values. Expected outcomes elsewhere in the section are prefixed `expected:`.

## 3. Commands run and their observed output

Reads (all read-only, all in the lane):

    python3 -c 'json.load(open(".ufo/waves/round-38/claims.json"))'      -> C1 depth:verifiability 4/held 4, C2 coverage 7/held 7
    wc -l SCORECARD.md                                                -> 1509
    grep -n 'Round-3[78]' SCORECARD.md                                -> 1496:## Round 37 result (only round heading in tail)
    cat c1-controls/before.txt, c2-controls/before.txt, census-before.txt -> before-state quoted in §2 above
    sed -n '120,200p;324,401p;417,442p;700,770p' corpus/instruments/r37-closure.sh -> E1/E12 helpers and check bodies
    ls .ufo/waves/round-38/wave1/                                     -> no pre-existing ScribeScorecard.* files

Draft creation (scratch `S=/fast/scratch/hyaku/kasegi-r38/ScribeScorecard`, created with `mkdir -p`):

    wc -l   $S/ScribeScorecard.*.md  -> 1 / 12
    sha256sum $S/ScribeScorecard.*.md -> e9f0c1e1…(correction), 65ff1df6…(section, pre-refinement)

Constraint harness over the composed SCORECARD (Python reimplementation of the shapes the frozen
checks test; section = `^## Round 38` to next `^## ` heading):

    G5/A section lines containing "Final lane commit:"            -> 0
    G5/B lines beginning "Correction (round 38)"                  -> 1, with f3246559=True, anchor ancestor=True
    G2/C required string "judged head: export-ref of .ufo/waves/round-38/final-gates/all-gates.txt" in section -> 1
    G2/D forbidden regex (final (lane )?(head|commit)|judged head)[^|]*[0-9a-f]{7,40}, case-insensitive -> 0 hits
    item  "Measured before: freeze 9a10b02fe411bb8d9d71aed3b1d3a5949d50d16b" present as substring -> PASS
    item  axes rows: | depth:verifiability | 4 | 4 (held) |, | coverage | 7 | 7 (held) |, | depth:density | 9 | 9 | -> all present
    item  "[L1-MEASURE]" occurrences in section                    -> 3 (3 lines)
    G3    fixed strings ⟨pending, <fill>, filled by the L1, <LANE_HASH>, <r38- over the added lines -> 0 each
    G3    word-bounded TBD / TODO over the added lines             -> 0 / 0
    heading count "^## Round 38" in composed file                  -> 1

Carry-over compatibility (the r37 suite is run unchanged at G8 on REF, so my appended bytes must not
open E1/E12). Helpers reimplemented from the committed source (`e1_final_hashes`, `e12_section`,
`check_e1`, `check_e12`), then run over the composed bytes with read-only git:

    E1 scan start (last /^#{1,4} .*Round[- ]?37/)                  -> composed line 1496 "## Round 37 result"
    E1 40-hex sample ("Final lane commit" line + next 4 lines)      -> 7 occurrences / 3 unique:
         f3246559bed2fd085dde860e00247ce394f02bad,
         2387dcf6ccfefcfb703783387b9aade8fc82abfa,
         83975acc83df4bd8d5eaf463182ae615f2b64546
    E1 binding                                                      -> each: cat-file -e rc=0, merge-base --is-ancestor <h> a173b0c2 rc=0
    E1 placeholders / lane-hash markers in composed SCORECARD       -> 0 / 0
    E12 round-37 block (composed 1496–1512, 17 lines)               -> c20300df=1, anchor-ancestor=2, Final lane commit: e666d902=0

(Direct ancestry probes, same cwd: `f3246559…`, `2387dcf6…`, `83975acc…` all `exists ancestor-of-base=yes`;
`9a10b02…` `exists ancestor-of-base=NO`; base `a173b0c2…` resolves.)

An earlier run of the same harness reported `FAIL E1 every sampled 40-hex exists+ancestor`; the cause
was the invocation cwd (the fleet root, not a git repo), not the bytes — re-run from
`/home/vgpnk/Projects/shokunin/kasegi-shokunin` the binding line passes as recorded above. Recorded
here so the red is not read as a content defect.

## 4. Findings

1. **Correction placement is load-bearing** (see §1). The correction line must quote the literal
   `Final lane commit:` label, so it can never live inside the round-38 section: both G5's zero-line
   rule and G2's regex would fire. Landing it between the round-37 section and the round-38 heading
   satisfies G5's file-wide `>=1` line requirement and keeps both section-scoped rules green.
2. **E1 samples to EOF, not to the block end.** `e1_final_hashes` (`r37-closure.sh:324`) starts at
   the last round-37 heading and scans every later line for `[Ff]inal lane commit`, taking the next
   four lines. My correction line therefore adds three 40-hex values to E1's sample set. All three
   exist and are ancestors of the base, so E1's `bound == total` limb stays closed (verified above);
   a correction line naming an unresolvable or side-branch commit would open it.
3. **The freeze commit is not E1-visible.** `9a10b02…` is measured `exists` but **not** an ancestor of
   the base `a173b0c2…`; it appears only on the `Measured before:` line, which is 10 lines past the
   nearest `Final lane commit` trigger and outside its four-line window. So it cannot enter E1's
   binding set from this append.
4. **Exact-token spellings chosen for the greps.** The `judged head:` line carries no backticks inside
   the required substring so G2's literal test matches; the `Measured before: freeze <hash>` token is
   likewise unquoted so the item's literal string is a substring.
5. **No final-head labelling.** The section contains no `Final lane commit:`, no `final head`/`final
   commit`+hash line, and names J only by the all-gates receipt reference; the round-37 reference
   hash appears as `r37 reference 2387dcf6` in the evidence cell and on the `Measured after:` command
   line (`--export-ref 2387dcf6…`), both outside the labelled-head vocabulary.

## 5. Out of scope / not done

- Not executed: `corpus/instruments/r38-closure.sh` (absent at this seat's read) and
  `corpus/instruments/r37-closure.sh` — the latter's default scratch root is
  `/fast/scratch/hyaku/kasegi-r37`, which G6 watches live; running it would create the very entry G6
  red-flags. E1/E12 were re-derived from the committed helper sources instead.
- Not touched: `SHONEN.md` (round-38 lines are another seat's deliverable), `PROVINCE.md`,
  `corpus/README.md`, `corpus/lessons/round-37.md`, `corpus/knowledge/considerthese-proposals-ledger.md`,
  any instrument, the judge, any commit.
- Writes made: the two deliverables, this receipt, and scratch. No tool install, no network fetch, no
  mutating git/jj command.

## 6. Scratch and quiescence

`S=/fast/scratch/hyaku/kasegi-r38/ScribeScorecard` (created with `mkdir -p`, all work under it) was
removed after the deliverables were copied:

    ls -d /fast/scratch/hyaku/kasegi-r38/ScribeScorecard -> exit 2, "No such file or directory"
    ls -1 /fast/scratch/hyaku/kasegi-r38 | grep -c '^ScribeScorecard$' -> 0
    ls -ld /fast/scratch/hyaku/kasegi-r36 /fast/scratch/hyaku/kasegi-r37 -> both "No such file or directory"

`kasegi-r38/` still lists 26 sibling seat directories belonging to other live seats at read time;
none of them is mine, and the G6 after-state is the integration seat's measurement.

## 7. Provenance

Inputs: `.ufo/waves/round-38/claims.json`; `.ufo/waves/round-38/c1-controls/before.txt`,
`c2-controls/before.txt`, `census-before.txt`; `SCORECARD.md` lines 1380–1509 and raw 1496–1509;
`corpus/lessons/round-37-verifier-spotcheck.md` §5 (D-D); `corpus/instruments/r37-closure.sh`
(header notes, `e1_final_hashes`, `check_e1`, `e12_section`, `check_e12`); the wave-1 spec item text
for `ScribeScorecard`, `ExecSuiteBuild` (G1–G8 texts), and `ExecDensity`. All lane git reads were
read-only (`cat-file -e`, `merge-base --is-ancestor`, `rev-parse`, `status --porcelain`).
