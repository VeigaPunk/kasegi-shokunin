# ScribeShonen — round 38: the four SHONEN.md round-38 lines

Seat `ScribeShonen`, role scribe, leaf (no subagent dispatch). Item: read `SHONEN.md` in full, draft
four `[~]` lines — one per promotion box — carrying round-38 evidence pointers, byte-exact to
`.ufo/waves/round-38/wave1/ScribeShonen.block.md`; the judged head is named only by reference; values
the L1 must fill are `[L1-MEASURE]`. No product code, judge, gate file or front-door file was edited;
nothing was committed, pushed or published.

## 1. Inputs read (read-only)

| Input | What it gave |
|---|---|
| `SHONEN.md` (178 lines) | the four box titles verbatim, the round-34/35/36/37 append style (`- [~] <box>` + 6-space-indented `— evidence (round N, …):`), and the round-37 lines' three-hash drift (D-B class) this round must not repeat |
| `.ufo/waves/round-38/claims.json` (72 lines) | C1 predicate G1–G8 and C2 counters; the G2 wording `judged head: export-ref of .ufo/waves/round-38/final-gates/all-gates.txt`; its ban on lines labelling a 7+-hex hash as a final/judged head (three label strings, quoted nowhere here); the G3 placeholder vocabulary (not reproduced here); G8 carry-over |
| `.ufo/waves/round-38/wave1-spec.json` | 73 seats and their roles (no hunt-to-claim seat) |
| `corpus/lessons/round-37-verifier-spotcheck.md` §5 | D-A (scaffolding pasted into `PROVINCE.md`/`corpus/README.md`), D-B (three heads named "final"), D-C (pending markers), D3, D-D (the r37 section tags hash `f3246559…` with a final-lane label), D-E (scratch leftover) |
| `corpus/knowledge/considerthese-proposals-ledger.md` heading | D-F context (empty `## Round-37 dispositions`) — no line of my block claims G7 |
| wave1 deliverables read for accurate pointers | `ScribeSkillRegistry.row.md` + `.md`, `ScribeFrontierBlocks.province-eof.md` / `.readme-eof.md` / `.readme-row.md`, `ScribeScorecard.section.md` / `.correction.md`, `ScribeLOG.block.md`, `ExecDensity.md`, `ExecFenceWalk.md`, `ExecC2Binding.md`, `ExecC2Audit.md`, `ExecC2Census.md`, `ExecC2Capture.manifest.json`, `ExecDeclaredBlocks.md`, `ScoutF21Sibling.md`, `ConnSibling.md`, `ExecQuiescence.md` |
| `kake-shokunin/corpus/knowledge/security-txt-publishing.md:63` (read-only sibling) | the adjacent mention quoted in box 4 |

## 2. Measurement (this seat, 2026-10-26T18:33Z–18:38Z)

Scratch `S=/fast/scratch/hyaku/kasegi-r38/ScribeShonen`; `TMPDIR=$S` exported; every copy and walk
under `$S`; `$S` removed at §7. Interpreter `python3` 3.14.8, `git` 2.56.0.

### 2.1 `SKILL.md` base and the appended-registry-row mirror

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
$ cp SKILL.md "$S/SKILL.base.md"
$ cat .ufo/waves/round-38/wave1/ScribeSkillRegistry.row.md >> "$S/SKILL.base.md"
$ wc -l -c SKILL.md "$S/SKILL.base.md"
  1113 110173 SKILL.md
  1114 111619 $S/SKILL.base.md
$ sha256sum SKILL.md "$S/SKILL.base.md"
dc6b94b0582ca0b1421fc614a5cdc5e4c557be7236b9221032b0ab7205d58b30  SKILL.md
0937bce505de6ac9ddd74115002e01aa51aabfa10b557495493021c619b7cd53  $S/SKILL.base.md
$ tail -c 1 SKILL.md | od -c        # 0000000  \n   (append cannot join lines)
$ python3 corpus/instruments/density.py SKILL.md --label base38 | tail -2
| | **mean dens** | | | | | | | | **229.1** |
Total path-citation instances: 760 across 27 blocks.
$ python3 corpus/instruments/density.py "$S/SKILL.base.md" --label plus-r38-row | tail -2
| | **mean dens** | | | | | | | | **233.1** |
Total path-citation instances: 768 across 27 blocks.
$ KASEGI_LANE_ROOT=$PWD python3 corpus/instruments/anchorcheck.py "$S/SKILL.base.md"
== …/SKILL.base.md: 16 in-range cite instances, 0 bad; 16 distinct anchors;
   LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0
exit=0
```

Block 27 in both runs: base `8 | 7 | 18 | 4 | 9 | 0 | 31 | 442.9`, mirror
`9 | 8 | 26 | 5 | 11 | 2 | 44 | 550.0`; blocks 25 and 26 print identically in both tables, so the
append moves only the block it lands in. Row deliverable verified at my read: 1 line, 1446 B,
sha256 `502bd887707d831599cd70a577c3c1fa139c3ad83199d6dafde5df659bce1efe`.

### 2.2 Base counters quoted in box 3

```
$ grep -cE '^\| F[0-9]+ \|' corpus/README.md                 -> 20
$ python3 corpus/instruments/frontier-recheck-count.py        -> entries=23 pass=23 exit=0
$ ls corpus/knowledge/*.md | wc -l                            -> 49
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md  -> 54
$ python3 corpus/instruments/recheck-audit.py --quiet
executes=25 gated=24 broken=0 … lines=49 total=49 pass=49 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=49 missing=0 unexpected=0 exit=0
```

### 2.3 Capture bytes quoted in box 2

```
$ sha256sum .ufo/waves/round-38/wave1/ExecC2Capture.S055.txt
63c8ad5271ef5dfb7edcf2c65b4555a2d81a82682fe4d31058d542880e11cd42  …/ExecC2Capture.S055.txt
$ wc -l -c < .ufo/waves/round-38/wave1/ExecC2Capture.S055.txt  -> 5146  272441
```

Manifest (`ExecC2Capture.manifest.json`): `http.status=200`, `fetched_utc=2026-10-26T18:25:51Z`,
`fetched_bytes=414858`, `snapshot_bytes=272441`, `lines=5146`, same `sha256`, no redirect.

### 2.4 Fence walk (box 4's end-state claim)

```
$ bash .ufo/waves/round-38/wave1/ExecFenceWalk.sh PROVINCE.md        -> closed
$ bash .ufo/waves/round-38/wave1/ExecFenceWalk.sh corpus/README.md   -> open
# mirror: base files + ScribeFrontierBlocks.province-eof.md / .readme-eof.md appended
$ bash …ExecFenceWalk.sh "$S/m2/PROVINCE.md"                        -> closed
$ bash …ExecFenceWalk.sh "$S/m2/corpus/README.md"                    -> closed
$ wc -l "$S/m2/PROVINCE.md" "$S/m2/corpus/README.md"                 -> 156  486
```

Base line counts and the D-A ranges, read on the lane bytes: `PROVINCE.md` 152 lines, the r37
amendment line at :80, `F21` count 0; `corpus/README.md` 454 lines, the lone fence opener at :426,
`## Round-37 admission` count 0, one F20 row. Reflows quoted in box 4: PROVINCE L79-L152 / L79-L80,
README L399-L454 / L426.

### 2.5 Dispatch shape and LOG state (box 2)

```
$ python3 -c 'Counter(role) over .ufo/waves/round-38/wave1-spec.json["items"]'
seats 73 {'executor': 21, 'scribe': 15, 'reviewer': 11, 'critic': 7, 'mutation-tester': 6,
          'scout': 6, 'connector': 3, 'sentinel': 2, 'simplifier': 2}
$ grep -c '^## Round 38' LOG.md            -> 0
$ grep -n '^## Round 3[5-7]' LOG.md        -> 1651, 1661, 1678 (`## Round 37` newest)
$ wc -l LOG.md                             -> 1692
```

### 2.6 Connector ruling (landed after my first draft)

`ConnSibling.md:53`: "**Q1 ruling: adjacent (kake field-pointer touch; reported, not absorbed) and
otherwise uncontested.**" The block's box-4 sentence matches both limbs: F21/S055 ground
"uncontested", kake's `CSAF` mention "adjacent, reported, not absorbed". `ScoutF21Sibling.md:45`
"**none**" held ground and `:55` "F21 is clear ground" corroborate.

## 3. Deliverable

`/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-38/wave1/ScribeShonen.block.md`

| Field | Value |
|---|---|
| Lines | **64** (`wc -l` → 64; last line 87 B; file ends with one `\n`) |
| Bytes | **5399** (`wc -c` → 5399) |
| sha256 | **`fc6b2603203b6f9bb3049df2ef369cea38fb6ba3c063b0cbab007ec842b28424`** |
| Structure | four `- [~] ` bullets separated by one blank line, each followed by 6-space-indented `— evidence (round 38…` continuation lines; no heading, no table, no validation text |
| Box titles | byte-equal to the four existing `- [~] ` box titles in `SHONEN.md` (checked with `grep -Fqx` against the unique title list → 4 MATCH) |

Only the landable bytes are in the file; the L1 appends it at EOF after the round-37 lines.

## 4. Validation of the block

```
$ grep -c '^- \[~\] ' ScribeShonen.block.md                                  -> 4
$ grep -n 'judged head: export-ref of .ufo/waves/round-38/final-gates/all-gates.txt' …
35:      reference — judged head: export-ref of .ufo/waves/round-38/final-gates/all-gates.txt — and the
58:      judged head: export-ref of .ufo/waves/round-38/final-gates/all-gates.txt.
$ grep -Fc <each of the three G2 head-label strings>                        -> 0 each
$ grep -Fc <each of the five frozen G3 placeholder strings>                   -> 0 each
$ grep -Fc '[L1-MEASURE]'                                                    -> 5
```

The reference phrase is kept whole on two single lines — an earlier draft wrapped it across a line
break, which a line-oriented G2 grep would have missed; that draft was corrected before filing.
No 7+-hex hash in the block is labelled as a final/judged head; the hashes present are the base
`a173b0c2`, the registry-row digest `502bd887…`, the capture digest `63c8ad52…`, and the two
round-37 block digests `cdfe44e3…` / `2ebd8cd2…`, none of them a head label.

Five `[L1-MEASURE]` slots, all integration-time values: (1) the landed `SKILL.md` line number and
digest; (2) the appended round-38 `LOG.md` entry position; (3) every measured value of the five
counters at the round-38 head; (4) the frontier row count at the head; (5) the declared-block
digests (`declared-blocks.txt` did not exist at 18:37Z: `ls` → No such file or directory).

## 5. Disclosures and limits

- **Expected ≠ observed.** `corpus/instruments/r38-closure.sh` does not exist in the lane at wave
  time (`ls` → No such file or directory; `ExecSuiteBuild` delivers
  `.ufo/waves/round-38/wave1/ExecSuiteBuild.r38-closure.sh`). Every suite result quoted in box 3
  (`closed=8/8`, `selftest cases=8 failures=0`, base red, exit 2 on a plain run) is the frozen C1
  contract written as the expected form, under the block's own umbrella sentence that all measured
  values at the round-38 head are `[L1-MEASURE]`. Likewise the C2 targets (`entries=24 pass=24`,
  `expected=50`, `records=45 bound=45`, census exit 0, frontier 21) are the frozen C2 expectations;
  the base limbs beside them are values I measured (§2.2).
- **Density row drift (calibration note).** `ExecDensity.md` §3–§4 measured a 598-byte draft row and
  reported the expected after-values `mean 230.8 / 765 cites`. The delivered row is
  `ScribeSkillRegistry.row.md` (1446 B), so those numbers do not describe the landed bytes; §2.1
  re-measures on the delivered row and the block quotes `233.1 / 768 cites`. If the L1 lands a
  different row, both figures move again and the block's mirror figures (`233.1`, `768`, block-27
  `44 / 550.0`) are the ones to re-take.
- **Pointer landed late.** Box 4 cites `.ufo/waves/round-38/wave1/ConnSibling.md`; at the time the
  block bytes were first written that receipt was still in flight. It landed before filing and I
  verified its Q1 ruling (§2.6), but the pointer preceded the artifact.
- **No-harm limbs attributed, not re-run by me:** the base `anchorcheck.py` figures quoted in box 1
  as reproduced (`ExecDensity.md` §2) are that seat's measurement; my own anchorcheck run is the
  mirror run in §2.1. The two round-37 block digests are the recomputation in `ExecDeclaredBlocks.md`
  §5 (2 lines / 295 B and 27 lines / 2947 B), not my own hash.
- **Box 2 is a negative claim.** "No new end-to-end domain task ran this round" rests on the
  dispatch role census (§2.5), the absence of a round-38 `LOG.md` heading at base, and the content
  of `ScribeLOG.block.md` (claims, both instruments, F21 admission, wave, tooling — no hunt). No
  domain task was executed by this seat and none is dispatched.
- **Judged-head wording.** The block never names a round-38 hash; the only head it names is by
  reference, and the r37 heads are not named at all (the round-37 D-B drift class). The lanes' base
  `a173b0c2` is labelled `base`, not "final".
- No file outside `.ufo/waves/round-38/wave1/` was written by this seat; `SHONEN.md` itself was not
  edited (append is the L1's integration step).

## 6. Tooling

No installs or upgrades; `python3` 3.14.8, `git` 2.56.0 and GNU coreutils sufficed. No pacman, no
network fetch (the capture quoted in box 2 was fetched by `ExecC2Capture`, not by me), no host
service touched, no config file edited.

## 7. Scratch

`/fast/scratch/hyaku/kasegi-r38/ScribeShonen` was created with `mkdir -p`, held `SKILL.base.md`,
`SHONEN.test.md` and `m2/`, and is removed after the block and this receipt were written
(`rm -rf -- "$S"`, then `test ! -e "$S"` verified). No other seat's scratch dir was touched.
