# ExecBaseRed — C1 base-red transcript at `a173b0c2b98c5ae39599fa9be76027fbbead0b9e`

Seat: ExecBaseRed (leaf). Round: kasegi-shokunin 38. Axis judged: `depth:verifiability`.
Item: export the round-38 base with plain commands and measure the G1–G8 defect state with
grep/awk/sha256sum, then run the r37 carry-over instrument over that export. No new suite was built.

Verdict: **every check that owns a base-content defect is RED at the base** (P0, G1–G5, G7). G6
(scratch quiescence) and G8 (r37 carry-over) are *live-state* readings: they cannot be green while
the wave is in flight, and the base export only reads green when the lane itself is quiescent at the
exported ref. Measured: `r38-closure.sh` absent; G1–G5, G7 red on content; G6 red mid-wave; G8
`closed=13/14 exit=1`, not the `14/14` the freeze recorded — the divergence is explained and
isolated below, and it routes one constraint to the round-38 suite builder.

## Deliverable

| Path | Lines | Bytes | sha256 |
|---|---|---|---|
| `.ufo/waves/round-38/wave1/ExecBaseRed.base-red-transcript.txt` | 254 | 13733 | `eee9569cb1d91eb7fc5a2bbb6da5d6eac09152c7d472b9ac4e4db6cb4645b51e` |

The file is the raw command/output transcript of one scripted run, copied from scratch and verified
byte-identical with `cmp` (exit 0). Section anchors inside it: P0 L15, P1 L22, G1 L33, G2 L74,
G3 L110, G4 L152, G5 L163, G6 L176, G7 L185, G8 L205, G8 diagnostic L236, end L254.

## Method and provenance

```
$ git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin rev-parse a173b0c2b98c5ae39599fa9be76027fbbead0b9e^{commit}
a173b0c2b98c5ae39599fa9be76027fbbead0b9e
$ git -C … merge-base --is-ancestor a173b0c2… 9a10b02f…        # [rc=0]: base precedes the claims freeze
$ git -C … archive a173b0c2… | tar -x -C /fast/scratch/hyaku/kasegi-r38/ExecBaseRed/b
export file count: 7290
```

All content measurements ran inside that export (`cd $S/b`); live-lane reads (`git status`, `git log`,
`git ls-tree`, `git cat-file`, `git show`) were read-only against the lane. No mutating git/jj
command, no network fetch, no tool install or upgrade, no subagent, no `agent://all` message.
`TMPDIR` was bound to the seat scratch dir; `--work` trees stayed under it.

Historical reads use `git show <ref>:<path> | grep` (no shell redirect), so every line number quoted
here is the file's own. A first draft piped such reads through the run-echo wrapper with `>`, which
shifted the bootstrap line numbers by two; the delivered transcript carries the clean form, and the
numbers below match it.

Instrument provenance for G8 (`0da98e37…` is the digest frozen in the r37 receipt):

```
$ git -C … cat-file blob a173b0c2…:corpus/instruments/r37-closure.sh | sha256sum
0da98e37b5a87e0ca7cb3d5f05ea05b992adbc4091095276848818a30342434d  -
   1558   73132
$ sha256sum /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r37-closure.sh
0da98e37b5a87e0ca7cb3d5f05ea05b992adbc4091095276848818a30342434d  …
```

Base-tree digests for the fixture work (all transcript-verifiable):

| File at base | `wc -l` | sha256 |
|---|---|---|
| `PROVINCE.md` | 152 | `3e9e66b2448d61b6d24bb66562b865c777593df55b27300252b94620503838ea` |
| `corpus/README.md` | 454 | `20c86fb2295726cc8c8b8b7ce24ae057d35dc1d1e6c5c3a2b860c67dab9f0365` |
| `SCORECARD.md` | 1509 | `1047ba2bcd02b462b79fbb1b14098eb7ee49d6af07b6a9ca47e908ca0ce470ee` |
| `SHONEN.md` | — | `f63256441798d15eedf76c7d3e5075ecf9890509b27ae741197eeb62075b9bef` |
| `corpus/lessons/round-37.md` | 335 | `8f5e49e729c3c1206f17934465f53d54d50a79f256462a337e9956b87369a2a2` |
| `corpus/knowledge/considerthese-proposals-ledger.md` | 43 | `fbcbfd193d17a244ca554e53cad835cdce3aee235df9c94097f62c625f2576b0` |

## Per-check RED/GREEN table

Expectation = what the round-38 claim requires the check to say about the *unfixed* base.

| Check (defect) | Expected at base | Observed at base (transcript anchor) | Verdict |
|---|---|---|---|
| P0 — the claim's own instrument | absent | `ls corpus/instruments/r38-closure.sh` → `No such file or directory` `[rc=2]`; 0 blobs at the ref; 99 other `corpus/instruments/` entries (L15–21) | **RED** (suite does not exist) |
| G1 (D-A) — front-door corrections, fence state, declared blocks | red: no correction lines, fences open at EOF, no declared-blocks file | `grep -c '^Correction (round 38)'` → **0** in `PROVINCE.md` and `corpus/README.md`; tree-wide byte search for `Correction (round 38)` → **0 files**; `PROVINCE.md` fences L81/L96/L124 (odd → `open_at_eof=1`), `corpus/README.md` fence L426 → `open_at_eof=1`; `ls .ufo/waves/round-38/declared-blocks.txt` → `No such file or directory` `[rc=2]`; scaffolding still present: `PROVINCE.md:90` `## 3. Deliverable B — …`, `PROVINCE.md:134` / `corpus/README.md:436` `## 4. Validation on a scratch mirror`; `^## Round-37 admission` in README → **0**; r37 appends `PROVINCE.md` L79–152 (**74** added, `git diff -U0` hunk `@@ -78,0 +79,74 @@`) and `corpus/README.md` L399–454 (**56** added, `@@ -398,0 +399,56 @@`); F20 rows 1/1 (L33–73) | **RED** |
| G2 (D-B) — all-gates v2 receipt, judged head by reference | red: no round-38 receipt; r37 receipt grades an ancestor; front doors name another head | no `.ufo/waves/round-38/final-gates/` entries (0); r37 receipt is `all-gates v1`, `export-ref=9492c776…`, `suite-sha256=0da98e37…`, `run-utc=2026-10-26T18:00:21Z`, 14 closed E-lines, `closed=14/14 exit=0`, `selftest cases=14 failures=0`; the r37 judged head `2387dcf6…` appears **0** times in `SCORECARD.md`/`SHONEN.md`, while `aa88877b` appears 1× and 2× (`SHONEN.md:172` "final lane head aa88877b…") (L74–109) | **RED** |
| G3 (D-C) — pending markers, stale line, widened placeholders | red: 7 pending markers, no resolutions section, stale L85 | `grep -c '⟨pending'` → **7** at L10, 90, 95, 216, 265, 300, 320; `grep -c 'Pending-marker resolutions (round 38)'` → **0**; `corpus/lessons/round-37.md:85` reads `… but is **not landed**.` — `grep -cF 'is not landed'` → **0** because of the markdown bold, `grep -n 'not landed'` → 1 hit; widened-token scan `<r3[0-9]-[a-z-]+>\|<fill>\|<LANE_HASH>\|<FRONTIER_N>`: SCORECARD 0, SHONEN 0, **LOG.md 2** (historical `<LANE_HASH>` at `LOG.md:1616`, `LOG.md:1632`), PROVINCE 0, lesson 0, README 0; the r37 bootstrap `9492c776` that the old E1 passed carried **3 placeholder lines / 4 token occurrences**: `SCORECARD.md:1505` `<r37-final-head>`; `SHONEN.md:172` `<r37-final-lane-hash>` + `<fill>`; `SHONEN.md:176` `<r37-final-lane-hash>` (L110–151) | **RED** |
| G4 (D3) — dispatch/results parity, closure order | red: results file absent at the r37 judged head; no round-38 pairs | `results.json` at `2387dcf6…` → **0** (82 tree entries); it exists only at `83975acc…` (`2026-10-26T15:03:15-03:00`), i.e. **107 s after** the judged head `2387dcf6…` (`15:01:28-03:00`); round-38 `dispatch.json` **0** and `results.json` **0** at base; the freeze tree `9a10b02` holds only `claims.json`, `c1-controls/before.txt`, `c2-controls/before.txt`, `census-before.txt` (L22–32, L152–162) | **RED** (and vacuous at base: no round-38 pair exists to compare) |
| G5 (D-D) — `Final lane commit:` label, round-38 correction | red: 1 stale label, 0 correction | round-37 section (`awk` from `^## Round 37`) `grep -c 'Final lane commit:'` → **1** (`SCORECARD.md:1509`, `Final lane commit: f3246559… (round-37 wave-evidence ancestor; …)`); `grep -c '^Correction (round 38)'` → **0**; `f3246559` resolves to a commit (L163–175) | **RED** |
| G6 (D-E) — live scratch quiescence kasegi-r36/r37/r38 | filing-time green; not a base-content property | `/fast/scratch/hyaku/kasegi-r36 dir=absent any_entries=0 seat_dirs=0`; `kasegi-r37 dir=absent any_entries=0 seat_dirs=0` (the r37 leftover file is gone); `kasegi-r38 dir=present any_entries=228805 seat_dirs=29` at 18:30:09Z — the count moves as peers start (it was 51558/13 nine minutes earlier) (L176–184) | **RED at measurement** (expected mid-wave) |
| G7 (D-F) — ledger round-37 dispositions | red: heading with empty body | `## Round-37 dispositions` at `L37`; body L38–L40 are empty, next section starts L41, `non_empty_body_rows=0`; 0 disposition-shaped rows; the file is 43 lines and holds **16** other `^|` rows, so a whole-file pipe-row count would be green by accident (L185–204) | **RED** |
| G8 carry — `r37-closure.sh` over the base export | freeze recorded `closed=14/14 exit=0` | `bash …/r37-closure.sh --export-ref a173b0c2… --work $S/r37w` → 13 closed E-lines, **`E9 … closed=0`** (`status-dirty=3, head-match=0`), `closed=13/14 exit=1` (L205–235) | **RED at measurement** — see next section |

## The G8 divergence (base export reads 13/14, not the frozen 14/14)

`before.txt` recorded `closed=14/14 exit=0` at freeze, when the live lane *was* the base and its
porcelain was empty. The r37 suite documents E9 as live by construction (`r37-closure.sh:93-100`,
`:155-170`): limb (b) reads the **live lane's** `git status --porcelain` exit-status and line count,
limb (c) scans the live scratch root, limb (d) requires the exported ref to **equal the live HEAD**.
At measurement the lane was `7001535` with three untracked round-38 wave entries, so
`head-match=0`, `status-dirty=3`.

Isolation run (L236–253), same instrument with `--export-ref` set to the live HEAD:

```
E9 payload=status-read=ok,status-dirty=3,scratch-seat-dirs=0,head-match=1,lane-root=1,scratch-root=absent closed=0
closed=13/14 exit=1
E-lines closed=1: 13 / 14
```

`head-match` flips to 1 and the residual red is `status-dirty`, the in-flight wave's own untracked
files. So the base’s 13/14 is a live-state reading, not a content difference at `a173b0c2`: the base
content passes all 13 ref-independent checks, and can read 14/14 only in a quiescent lane whose HEAD
equals the exported ref. Consequence for round 38: the frozen G8 wording (“carry-over r37-closure.sh
**on REF**”) is achievable only against the judged head J at filing (HEAD == J, porcelain empty, no
leftover seat dirs, scratch cleaned). Running the carry against base mid-wave reads 13/14 by design —
a suite that asserts 14/14 on a historical non-HEAD ref is unsatisfiable.

## Findings routed to the round-38 suite builder

1. **G3’s placeholder limb must be scoped to added lines.** `LOG.md` legitimately holds 2 historical
   `<LANE_HASH>` mentions (`:1616`, `:1632`) describing past rounds; a whole-file scan of the widened
   vocabulary false-reds on untouched base text. The frozen scope (“lines added base..REF”) is right.
2. **D-C’s stale line is markdown-bolded.** `corpus/lessons/round-37.md:85` says “is **not landed**”,
   so a literal `is not landed` grep returns 0 while `not landed` returns 1. A limb written as the
   literal phrase passes the defect it exists for.
3. **G1’s declared blocks cannot be the r37 append widths.** At base the appends are 74 lines
   (`PROVINCE.md` L79–152) and 56 lines (`corpus/README.md` L399–454); the amendment targets are the
   2- and 27-line blocks named in the r37 spot-check. `declared-blocks.txt` must declare the
   *round-38* block bytes and the equality limb must compare appended bytes to that declaration.
4. **Both front doors are open at EOF today** (`PROVINCE.md` from L81, three fences; `corpus/README.md`
   from L426, one fence). The fence limb must fail when the last fence opens inside an appended block
   and never closes, and must tolerate the ```` ```text ```` info string at `PROVINCE.md:96`.
5. **G7 must scope the row count to the section body.** The ledger already has 16 `^|` rows in other
   sections; a whole-file count is green while the round-37 body is empty (L38–L40, 0 rows).
6. **G2 must not require a literal J hash in SCORECARD/SHONEN.** At base neither file contains
   `2387dcf6…` (0/0) and both name `aa88877b` instead — exactly the drift D-B records. The limb
   should read the receipt’s `export-ref=` and assert the front doors cite the receipt, not a hash.

## Compliance

Writes: only `.ufo/waves/round-38/wave1/ExecBaseRed.base-red-transcript.txt` (deliverable) and this
receipt; everything else under `/fast/scratch/hyaku/kasegi-r38/ExecBaseRed/`, removed before yield.
No lane/fleet/shokuknow or source-tree edits; no mutating git; no `pacman`; no installs; no network
fetches; no subagent dispatch.
