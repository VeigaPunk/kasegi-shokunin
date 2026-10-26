# ScribePendingResolutions — round-38 receipt

Seat: ScribePendingResolutions (scribe, leaf). Lane: `kasegi-shokunin`. Milestone: round-38. Judged on
`depth:verifiability`. Item: draft the `## Pending-marker resolutions (round 38)` section for
`corpus/lessons/round-37.md` and deliver it byte-exact as
`.ufo/waves/round-38/wave1/ScribePendingResolutions.block.md`.

## 1. Behavior

Delivered one landable block, 14 lines, sha256
`baf6c6b25933f5c1edc7b2e2b2bf68df4574ab8050339500f183db76e31b1a0b` (5,052 B): heading
`## Pending-marker resolutions (round 38)`, one append-only sentence, a 4-column table with 8 data rows —
one per base marker line L10, L90, L95, L216, L265, L300, L320 plus the L85 "is not landed" sentence — and
no other text. Every resolved value was read from committed bytes at the round-37 lane tip
`83975acc83df4bd8d5eaf463182ae615f2b64546`, the round-37 judged head
`2387dcf6ccfefcfb703783387b9aade8fc82abfa`, the integration commit
`0acffc82fa860a6cc4ff6190df2a7bd2036345fd`, or the fence commit
`aa88877bf921d952137817b91ca76234b206da65`; no value is inferred from prose alone, and the one place where
the committed record does not match the marker's own claim (L265) is reported as such rather than smoothed.

Base marker inventory (`git show 83975acc:corpus/lessons/round-37.md | grep -c '⟨pending'` → `7`; the
per-line reads `sed -n '10p;85p;90p;95p;216p;265p;300p;320p'` name the eight deferred items). Working tree
`corpus/lessons/round-37.md` sha256 `8f5e49e729c3c1206f17934465f53d54d50a79f256462a337e9956b87369a2a2` equals
the blob at `83975acc`, so the cited line numbers are the tip's.

## 2. Resolution evidence, row by row

| row | derivation command (all `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin`) | observed |
|---|---|---|
| L10 | `log --format='%h %s' b56a4168..83975acc`; `diff --numstat 2387dcf6 83975acc`; `show 2387dcf6:SHONEN.md \| grep -nE '2387dcf6\|aa88877b\|final'`; `show 2387dcf6:SCORECARD.md` § Round 37 | 9 round commits; the tip adds only `.ufo/waves/round-37/kasegi-r37-build-results.json` (`392 0`); SHONEN `:172` and `:176` name `aa88877bf921d952137817b91ca76234b206da65` as the "final lane head" and bind the suite run to it; SCORECARD carries `Final lane commit: f3246559…` |
| L85 | `show 0acffc82:corpus/knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md` head; `wc -l` | `source: S054` L3, `verified-at: 2026-10-26` L4, `ground: F20` L5, runnable `recheck:` L6; 84 lines |
| L90 | `cat-file -e 83975acc:corpus/knowledge/ssvc-…md`; `show 83975acc:… \| wc -l`; `log --format='%h %s' 0acffc8..83975acc -- corpus/knowledge/ssvc-…md` | exit 0; `84`; log empty (no later round-37 edit) |
| L95 | `grep -n 'S054:sha256 OK'` over `.ufo/waves/round-37` at the tip; `show 83975acc:.ufo/waves/round-37/wave1/ExecC2Harness.md` `:218-235`; spotcheck `:95` | transcript at `ExecC2Harness.md:225-230` (`S054:sha256 OK`, Q1/Q2/Q3 at anchors 6/7/14, `EXIT=0`) over the *mirrored* manifest; `all-gates.txt` holds no C2 limb; landed manifest anchors re-derived by the non-author as 259/277/473/68 with `occurrences=1` each |
| L216 | `show 83975acc:.ufo/waves/round-37/final-gates/all-gates.txt` counters; `diff --name-only aa88877b 83975acc -- <that path>`; spotcheck `:50-56` | 121 lines; `all-gates v1` :1, `export-ref=9492c776…` :2, `suite-sha256=0da98e37…` :3; 14 `payload=… closed=1` lines :8-:21; `closed=14/14 exit=0` :22 (exactly one); 14 `selftest case=` lines :31-:113; `selftest cases=14 failures=0` :114 (exactly one); diff aa88877b→tip empty (byte-identical) |
| L265 | `grep -n '7c232983'` at the tip; `ls-tree -r --name-only 83975acc \| grep -c '^corpus/considerthese-ledger.md$'`; `show 83975acc:corpus/knowledge/considerthese-proposals-ledger.md \| grep -n 'Round-37 dispositions'`; `show aa88877b` / `show 0acffc82` the same | block committed only in the seat receipt `ScribeConsiderthese.md:56` (9,184 B, sha256 `7c23298319a581720a5a66f63ea0b97ca65f2b9f3dd858bfd019fd86abc43706`); `corpus/considerthese-ledger.md` absent from every tree (count `0`); the heading `## Round-37 dispositions` sits at `:37` of the existing ledger from `0acffc82` onward and is followed by blank lines (no rows) |
| L300 | spotcheck `:98`, `:142-143`; `show 83975acc:.ufo/waves/round-37/wave1/ExecCensusReplay.md` `:11-13,84-87` | `W04 S028`, `W04 S029` (standing duplicate-URL warnings), `ok`, exit 0; registry 53→54 |
| L320 | `diff --numstat b56a4168 2387dcf6 -- . ':!.ufo'`; spotcheck `:105-111` | zero deletions on all 18 changed files (SKILL.md `2/0`, SCORECARD.md `15/0`, PROVINCE.md `74/0`, corpus/README.md `56/0`, corpus/SOURCES.md `1/0`, corpus/QUALITY.md `14/0`, LOG.md `17/0`, SHONEN.md `9/0`, `c2-controls/junk-f20.md` `41/0`, `r37-closure.sh` `1558/0`, entry `84/0`, ledger `8/0`, lesson `335/0`, S054 capture `518/0`, manifest `57/0`, `knowledge-expected.txt` `1/0`) |

## 3. Deliverable validation

- Banned-token sweep: `grep -nF -e '⟨' -e '<fill>' -e 'filled by the L1' -e '<LANE_HASH>' -e '<r38-' -e 'TBD' -e 'TODO'` on the block → no match (exit 1). The block contains no `⟨`/`⟩` at all, so the `⟨pending` token cannot recur.
- Table shape: 8 data rows (`grep -cE '^\| L[0-9]+ \|'` → 8); every row and the header carry exactly 4 columns (pipe count 5 per line, escaped `\|` inside cells accounted for).
- Append-only proof on a scratch copy: `cp corpus/lessons/round-37.md $S/lesson-append.md` + one blank line + the block → `grep -c '⟨pending' $S/lesson-append.md` → `7` (unchanged; the block adds none).
- Sizes: block `wc -l` → 14; `sha256sum` → `baf6c6b25933f5c1edc7b2e2b2bf68df4574ab8050339500f183db76e31b1a0b`; `wc -lc` → 14 lines, 5,052 B (two of the three citation line-numbers were fixed in place after the first write: `ExecC2Harness.md:224-231`→`:225-230`, spotcheck `:84-88`→`:50-56`, ledger `:28`→`:37`).
- Every cited range was read back at the cited ref: spotcheck `:8-9` (A and tip), `:50-56` (committed gate evidence), `:90` (`^source: S054` 0→1), `:95` (Q1–Q4 anchors), `:98` and `:142-143` (census), `:105-111` (harm check); `ExecGateReviewPrep.md:48` (`## 2. The all-gates v1 format contract`) and `:107` (`E10.5` R3 rule); `ExecCensusReplay.md:11-13,84-87`.
- Commit prefixes used resolve: `0acffc82`→`0acffc82fa86…`, `aa88877b`→`aa88877bf921…`, `2387dcf6`→`2387dcf6ccfe…`, `83975acc`→`83975acc83df…`, `9492c776`→`9492c776724e…`.

## 4. Touched surfaces

Writes: `.ufo/waves/round-38/wave1/ScribePendingResolutions.block.md` (deliverable) and this receipt only.
Scratch: `/fast/scratch/hyaku/kasegi-r38/ScribePendingResolutions/` (held `ag.txt`, `lesson-append.md`),
removed before yield. No lane file was edited — in particular `corpus/lessons/round-37.md` is untouched
(working-tree sha still `8f5e49e7…`); landing the block is the L1's append. Read-only git only
(`log/show/diff/status/rev-parse/ls-tree/ls-files/cat-file/archive/grep`); no mutating git, no pacman, no
tool installed, no network fetch. Fleet repo and `shokuknow` were not written.

## 5. Findings

1. **L265's named landing path does not exist.** The r37 lesson says the ledger landed as
   `corpus/considerthese-ledger.md` (18 rows, sha `7c232983…`). At `83975acc` that path is in no tree
   (`ls-tree -r --name-only | grep -c` → 0); the byte-exact block exists only inside the seat receipt
   (`ScribeConsiderthese.md:56`), and the actual landing was an 8-line append to
   `corpus/knowledge/considerthese-proposals-ledger.md` (`0acffc82`, 8/0) whose `## Round-37 dispositions`
   heading at `:37` is followed by blank lines. This is exactly the L1-found D-F, now measured from bytes;
   the block records it as unresolved-at-37 with the round-38 ledger deliverable as the closure.
2. **L95 has no committed C2 transcript at the integrated head.** `all-gates.txt` is a C1-only receipt
   (E1–E14); the only committed S054 run is the seat's mirror run with planned anchors 6/7/14, not the
   landed anchors 259/277/473/68. The block says this plainly and points at the non-author byte
   re-derivation plus the entry's runnable `recheck:` line, rather than claiming a transcript that does not
   exist.
3. **L10 has three candidate heads in the record.** Judged head `2387dcf6`, lane tip `83975acc` (results
   file only), in-tree binding `aa88877b`. The block resolves L10 to `2387dcf6`/`83975acc` and names the
   `aa88877b` binding as the round-38 D-B correction target, so the row does not launder the drift.
4. **L216 is fully closed by bytes**: the gates file is byte-identical from its fence commit to the tip,
   its digest equals `r37-closure.sh` at the judged head, and its counters are unique (one
   `closed=14/14 exit=0`, one `selftest cases=14 failures=0`, 14 payload lines, 14 case lines).

## 6. Out of scope

No edit to `corpus/lessons/round-37.md` or any other lane/front-door file; no gating of the round; no
commit, push, judge, or report work; no r37/r38 claim measurement.

## 7. Artifacts

- `.ufo/waves/round-38/wave1/ScribePendingResolutions.block.md` — 14 lines, 5,052 B, sha256 `baf6c6b25933f5c1edc7b2e2b2bf68df4574ab8050339500f183db76e31b1a0b` (the landable bytes only).
- `.ufo/waves/round-38/wave1/ScribePendingResolutions.md` — this receipt.
