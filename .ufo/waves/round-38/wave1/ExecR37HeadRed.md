# ExecR37HeadRed — round-37 judged head vs tip: G1–G8 defect state (raw transcript)

Item: "Same as a base-red transcript but for the round-37 judged head `2387dcf6ccfefcfb703783387b9aade8fc82abfa`
and the round-37 tip `83975acc83df4bd8d5eaf463182ae615f2b64546`". Axis: depth:verifiability (C1, score 4).

Deliverable: `.ufo/waves/round-38/wave1/ExecR37HeadRed.transcript.txt`
= 881 lines, sha256 `a6cbf185cb7c1669c0937750ff453ba60224fd10b63a37bb9598dcee51778e95`, 51578 bytes.
It is the raw transcript (commands echoed with their real output and exit codes), produced by two scratch
scripts (`probe.sh`, `probe2.sh`) plus one appended read-only git section; no text in it is reconstructed.

## 1. Method

- Ref resolution/ancestry and all git reads: read-only git against
  `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (`cat-file`, `log`, `merge-base --is-ancestor`, `diff
  --name-only`, `ls-tree`, `rev-parse`, `status`). No mutating git command was run; the one `rm -rf` is
  inside my own scratch dir.
- Exports: `git -C <lane> archive <ref> | tar -x -C $S/exp-<tag>` for each head
  (`r37j` = 2387dcf6, `r37t` = 83975acc). Scratch `S=/fast/scratch/hyaku/kasegi-r38/ExecR37HeadRed`,
  `TMPDIR=$S`, all `--work` dirs under `$S`. Export sizes: 7288 files (r37j), 7289 files (r37t).
- G1–G8 are the round-38 check semantics from `.ufo/waves/round-38/claims.json` C1, applied to the r37
  bytes: each measurement reads only the export, except G6 (live by definition) and G8 (the suite, whose
  E9 limbs are live by design). `corpus/instruments/r38-closure.sh` does not exist yet (it is another
  seat's deliverable), so the defect state was measured with plain commands as instructed, not through it.
- Tooling: nothing installed or upgraded this seat. python3/bash/coreutils/git/tar as shipped.

## 2. Head identity and order (measured)

| ref | commit time (-0300) | subject |
|---|---|---|
| `9492c776724e737caf5815fabc98e59ea04830df` | 2026-10-26 14:59:49 | round-37: F1 bootstrap receipt (disclosed token edits: E10 green + summaries + selftest case) |
| `aa88877bf921d952137817b91ca76234b206da65` | 2026-10-26 15:00:25 | round-37: F2 final head — genuine all-gates transcript of the F1 run |
| `2387dcf6ccfefcfb703783387b9aade8fc82abfa` (r37 **judged head**) | 2026-10-26 15:01:28 | round-37: F3 final head — bind final lane hash in SHONEN/SCORECARD |
| `f3246559bed2fd085dde860e00247ce394f02bad` | 2026-10-26 13:59:17 | round-37: wave evidence — spec/plan/dispatch (kasegi-r37-build, 64 seats v2) |
| `83975acc83df4bd8d5eaf463182ae615f2b64546` (r37 **tip**) | 2026-10-26 15:03:15 | round-37: WAVE-DONE results — kasegi-r37-build-results.json (64/64 settled) |

`merge-base --is-ancestor 2387dcf6 83975acc` → exit 0; `git diff --name-only 2387dcf6 83975acc` = exactly
`.ufo/waves/round-37/kasegi-r37-build-results.json`. All three older "final"-labelled heads
(`9492c776`, `aa88877b`, `f3246559`) verify as ancestors-or-equal of `2387dcf6` (each
`merge-base --is-ancestor … 2387dcf6` exit 0). Lane HEAD at measurement: `700153593eb586c70a6499c8ca225ee4d673bc9b`.

## 3. G1–G8 defect state (as measured; `open` = defect present, i.e. the round-38 check would be RED)

| check (defect) | measured at 2387dcf6 | measured at 83975acc | state |
|---|---|---|---|
| **G1** (D-A front-door scaffolding) | `grep -c '^Correction (round 38)'` PROVINCE.md=`0`, corpus/README.md=`0`; PROVINCE.md=152 lines, README=454 lines; scaffolding anchors present (PROVINCE L83 `\| property \|`, L90 `## 3. Deliverable B — corpus/README.md block`, L126, L134 `## 4. Validation on a scratch mirror`, L137 `ScribeFrontierAmendments/mirror`, L140 `\| check \|`; README L436/L439/L442); `grep -c '^## Round-37 admission'` README=`0`; fence walk at EOF PROVINCE=**closed** (L81 open, L96 ````text` content, L124 close), README=**OPEN (unbalanced)** (L426 open, never closed); `.ufo/waves/round-38/declared-blocks.txt` absent; PROVINCE L79-80 sha256 `cdfe44e3…` (295 B) = its declared digest; README's declared 27-line block `2ebd8cd2…` matches **no** 27-line window in README.md, but matches PROVINCE.md L97-123 | identical (r37t differs only by the results file) | **open** |
| **G2** (D-B judged-head drift) | all-gates first line `all-gates v1` (0 × `all-gates v2`); `export-ref=9492c776…`, `suite-sha256=0da98e37…` (= the committed and executing suite bytes), `run-utc=2026-10-26T18:00:21Z`; 14 × `E<n> … closed=1`, `closed=14/14 exit=0`, `selftest cases=14 failures=0`; the graded ref is not the head: `git diff --name-only 9492c776..HEAD` = **3** files (all-gates.txt, SCORECARD.md, SHONEN.md) | same header; diff = **4** files (+ `kasegi-r37-build-results.json`); labels: SCORECARD L1509 `Final lane commit: f3246559…`, SHONEN L172 `final lane head aa88877b…`, receipt `9492c776`, judged head `2387dcf6` — four distinct heads named by one round | **open** |
| **G3** (D-C pending markers) | `grep -c '⟨pending' corpus/lessons/round-37.md` = **7** (L10, L90, L95, L216, L265, L300, L320); `Pending-marker resolutions (round 38)` = 0; L85 `… but is **not landed**.` present (1); widened-vocabulary hits on lines added `b56a4168..REF` = **10** (`⟨pending` 7, `filled by the L1` 1, `<LANE_HASH>` 1, `TBD` 1, `TODO` 2) | identical | **open** |
| **G4** (D3 closure order) | `.ufo/waves/round-37/wave1-dispatch.json` with `taskCall.tasks` = **64**; **no** `*-results.json` (`ls` exit 2; `git ls-tree … kasegi-r37-build-results.json` = **0** lines) | `kasegi-r37-build-results.json` tracked (`git ls-tree` = 1 line, blob `22f7fdbc…`, 326389 B) and parses to `seats=64, results=64` | **open at 2387dcf6, paired only at the tip**, and then under a name that is not `wave1-results.json` |
| **G5** (D-D label drift) | SCORECARD round-37 section = L1496 `## Round 37 result` → EOF; exactly **1** `Final lane commit:` line (L1509 `f3246559…`, parenthetical "round-37 wave-evidence ancestor"); L1507 `Anchor ancestor (r36 lane head): c20300df…`; `grep -c '^Correction (round 38)' SCORECARD.md` = **0**; `f3246559` occurs once in SCORECARD.md and **nowhere** in SHONEN.md or the round-37 lesson | identical | **open** |
| **G6** (D-E scratch quiescence, live) | `/fast/scratch/hyaku/kasegi-r36` **absent**, `/fast/scratch/hyaku/kasegi-r37` **absent**, `/fast/scratch/hyaku/kasegi-r38` present with **20** seat dirs (19 siblings + this seat, mid-wave) | same (live, ref-independent) | r36/r37 quiescent now; the verdict's named leftover (`kasegi-r37/build-spec.py`) no longer exists |
| **G7** (D-F empty ledger section) | `corpus/knowledge/considerthese-proposals-ledger.md` = 43 lines; `## Round-37 dispositions (appended 2026-10-26, R31 home)` at **L37**; non-empty body lines under it = **0** (`cat -A`: L38-L40 empty, next heading L41 `## Re-pin note`); `Round-37 dispositions — filled (round 38)` = 0 | identical | **open** |
| **G8** (carry-over suite) | `bash corpus/instruments/r37-closure.sh --export-ref 2387dcf6 --work $S/w/r37j` → **`closed=13/14 exit=1`**, sole red **E9** (`status-read=ok,status-dirty=3,scratch-seat-dirs=0,head-match=0,lane-root=1,scratch-root=absent`); E1–E8, E10–E14 all `closed=1` | `--export-ref 83975acc` → **`closed=13/14 exit=1`**, identical payloads | **red at both** (E9 only) |

Suite identity: `corpus/instruments/r37-closure.sh` sha256
`0da98e37b5a87e0ca7cb3d5f05ea05b992adbc4091095276848818a30342434d` in the working tree **and** at both
refs (blob `68ac41e8fdab46ba508800a377f396e663f2a436`, 73132 B, 1558 lines) — the instrument is unchanged
across the r37 tail and since, so the r37→r38 carry-over bytes are stable.

Both heads print `closed=13/14 exit=1` with **only E9** red. E10 passes at both, i.e. the v1 all-gates
receipt's shape, digest, ancestry and cross-run payload keys all validate against the r37 heads: the D-B
defect is **which head the receipt names and what changed after it**, not the receipt's shape.

## 4. Findings the L1 / suite builder needs

1. **D3/G4 evidence is exact and asymmetric.** `2387dcf6` (judged head) carries the 64-seat dispatch and
   **no** results file; `83975acc` adds `kasegi-r37-build-results.json` (seats=64, results=64) at
   15:03:15, i.e. **28 s after** the verdict's recorded `complete kasegi round=37` at 15:02:47
   (`corpus/lessons/round-37-verifier-spotcheck.md` §5 D3; the completion timestamp is not in git). The
   results file is named `kasegi-r37-*`, not `wave1-*`: a `*-results.json` glob pairs it, a
   `<dispatch-basename>-results.json` rule does not. Round-38's G4 must state which rule it uses.
2. **The fence limb needs a real CommonMark walk.** A naive count of bare vs info-string fence lines
   labels PROVINCE.md unbalanced (2 bare + 1 info at L81/L96/L124); the toggle walk gives PROVINCE
   **closed** at EOF and README **open** (single unclosed fence at L426). Only README is red on that limb
   — a parity counter would have failed a file that is fine and hidden the one that is not.
3. **A declared block can move between files.** README's declared 27-line block (`2ebd8cd2…`, 2947 B) does
   not exist as any contiguous window of README.md at either head; the same 27 lines sit inside
   PROVINCE.md L97-123 (in a ````text` fence). G1's "the file's last `<lines>` lines hash to `<sha256>`"
   must stay per-file and per-line-count; a repo-wide digest search would call this closed.
4. **Placeholder vocabulary self-reference.** 3 of the 10 hits on r37's added lines are the r37 suite's own
   bytes (its E1 header comment quoting `filled by the L1` / `<LANE_HASH>`, plus `TODO` in its receipt
   fixtures). Round-38's G3 exclusion of `r38-closure.sh`/`r38-fixtures` is what keeps that from being a
   false positive; with base `a173b0c2` the r37 suite is outside the diff, so the hazard does not bite this
   round — but the exclusion is load-bearing, not cosmetic.
5. **G8's 14/14 is time-dependent.** `check_e9` takes `want=${5:-$ref}` and the CLI's `run_suite_report`
   passes no extra argument, so E9 limb (d) requires **live lane HEAD == exported ref**, and limb (b)
   requires a clean worktree. Measured now: both r37 exports are worth 13/14, and the live tree is dirty
   from round-38 wave evidence (`status-dirty=3`). A round-38 G8 that shells out to the r37 CLI can print
   `closed=14/14` only while the lane HEAD is exactly REF and the tree is clean; after the receipt commit Y
   (= J + receipt) that is no longer true. Two ways out: run G8 during the all-gates run when HEAD==J
   (before Y exists) and record that, or have r38-closure.sh call the r37 check functions directly and pass
   an explicit EXPECTED_HEAD (the function signature already supports the fifth argument). This is the one
   measurable risk to C1's G8 wording.

## 5. Scope, no-harm, cleanup

- Writes: this receipt and the transcript deliverable under
  `.ufo/waves/round-38/wave1/`, plus scratch under `/fast/scratch/hyaku/kasegi-r38/ExecR37HeadRed/`.
  No tracked lane file was modified: `git -C <lane> diff --stat HEAD` is empty; `git status --porcelain`
  shows only the pre-existing untracked round-38 wave paths.
- Scratch removed before yielding: `rm -rf -- $S` exit 0; `find /fast/scratch/hyaku/kasegi-r38 -maxdepth 1
  -name ExecR37HeadRed | wc -l` → `0`.
- No git mutation, no commit, no push; no message to `agent://all`; no subagent dispatch.
