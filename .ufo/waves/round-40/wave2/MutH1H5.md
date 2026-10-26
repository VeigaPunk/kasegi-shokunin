# MutH1H5 — round 40 wave 2 receipt (mutation probe, suite limbs H1–H5)

Seat: `MutH1H5` (mutation tester, leaf — no subagents dispatched). Wave:
kasegi-shokunin round-40 FALSIFY wave 2, dispatched by the L1 (KasegiR40, hyaku
run 9). Axes touched: **depth:verifiability** (primary), **coverage** (read-only
context). I authored none of the bytes under attack: the suite is the committed
`corpus/instruments/r40-closure.sh` at the judged head.

## Item attacked, command re-run, result

- **Item falsified:** the frozen C1 predicate's selftest clause — that the
  graded selftest (`--selftest --export-ref Y` → `selftest cases=10 failures=0`,
  one graded `selftest case=H<n> … verdict=pass` line per check) actually pins
  each check's defect-class closure for limbs **H1–H5**. Attack: one
  find→replace patch per limb that reopens exactly that check's defect class
  (H1 rename the suite/registry-row pattern; H2 weaken the correction grep; H3
  drop the M39-2 token; H4 drop the quote/date requirement; H5 trust receipt
  payloads again), then the suite's `--selftest` and the plain export run at Y
  per mutant; a limb is killed only when the mutant changes the verdict; any
  survivor is a defect.
- **Command re-run (green re-run evidence):** the two C1 counting commands at
  the Y fixture (below): plain `--export-ref <Y>` → `closed=10/10 exit=0` with a
  transcript **byte-identical to the committed receipt**, and `--selftest
  --export-ref <Y>` → `selftest cases=10 failures=0`, `judge=own-report
  accepted=1`, all six forged reports rejected.
- **Result: reproduced + defect found** — four limbs killed (H1, H2, H3, H5);
  **H4 survived** (selftest-coverage gap on the quote/date conjuncts; defect
  below). The committed suite itself is load-bearing on every probed clause
  (probe evidence under the H4 finding); the survivor is a gap in the graded
  fixture set, not a dead check.

## Environment

- Lane repo `/home/vgpnk/Projects/shokunin/kasegi-shokunin`: READ-ONLY to this
  seat (read-only git only: rev-parse/log/ls-tree/diff/status/show/archive/
  clone-source). Fleet root and `/home/vgpnk/Projects/shokuknow` untouched; no
  campaign tool run there.
- Suite bytes under test extracted from the judged head
  J=`3074c7679d6f527ec3930d7748ccce1dbae4a58a` via `git archive | tar -x`;
  pristine suite sha256 `bdbd18a3239c3467c79b5c487a8e3256c2cae1678752cea2487a5
  eaa12897f1e` — equal to the receipt's recorded `suite-sha256=` and to the
  declared-blocks whole-file declaration for the suite path (1734 lines).
- **Y materialized in the seat clone** (the receipt is untracked in the lane —
  `git log -- .ufo/waves/round-40/final-gates/all-gates.txt` is empty — so no
  lane commit carries it): `git clone` → detach at J → copy the lane's untracked
  receipt (sha256 `7b8cda36c793c5855fa6ffcb78d241fca47f0d3679b2d7c38f7a95904246
  3484`, byte-identical to the lane file) → commit with fixture identity
  (`r40-muth1h5@local`; `git rev-parse --show-toplevel` asserted == the clone
  dir before the commit) → **Y=`89cdbbe1c17d4fcb0cabb10148f898ab11e6ccc2`**;
  `git diff --name-only J Y` = `.ufo/waves/round-40/final-gates/all-gates.txt`
  only.
- Every run: `TMPDIR=$S/tmp`, `--lane $S/clone --work $S/w-<tag> --scratch-root
  $S/sroot` (sroot clean → H6 `strays=0`), identical args for
  pristine/mutated/restored runs. Scratch
  S=`/fast/scratch/hyaku/kasegi-r40/MutH1H5` removed before this receipt was
  finalized.
- Disk guard green before the pass (`/fast/scratch/hyaku` 24%, 615.5G free). No
  tools installed or upgraded (none needed; pacman untouched — paused
  host-wide; no network use).

## Baseline (pristine `bdbd18a3…`)

| run | command | result |
|---|---|---|
| R0-plain | `bash <pristine> --export-ref 89cdbbe1… --lane <clone> --work … --scratch-root …` | rc=0, `closed=10/10 exit=0`; transcript byte-identical to the committed receipt incl. `run-utc=2026-10-26T21:56:22Z` (deterministic re-tee) |
| R0-selftest | `bash <pristine> --selftest --export-ref 89cdbbe1… …` | rc=0, `selftest cases=10 failures=0`, `judge=own-report accepted=1`, six forged reports `rejected=1` |

Per-case mutant baseline: H1 3/3, H2 3/3, H3 2/2, H4 3/3, H5 2/2, H6 4/4,
H7 6/6, H8 2/2, H9 5/5, H10 3/3 — every line `positive=pass … verdict=pass`.

## Byte-self-binding (mode contamination — documented once, excluded from attribution)

Any byte mutation of the executing suite reds the export-bound limbs in ANY
full run, regardless of which check the patch touches: H1's digest limb
(executing bytes vs the export's copy), H7's receipt `digest`/`header-lines`/
`cmp` limbs, H9's declared whole-file tail-sha for the suite path, and the
H5/H7 payload-match cascades of those deltas. Observed identically in all five
mutant selftests (`case=H1 positive=fail` with `digest=0,registry=1` for the
non-H1 patches; `case=H5`/`case=H7` `positive=fail` with mutants counts
unchanged) and in every mutant plain run. Control: mutH4 committed into the
clone as Y4=`87644f31329ae0d6f0f2a5d358196eec4075c63e` (diff J..Y4 = the
receipt + the suite) and run matched-bytes → **H1 GREEN** (`digest=1`) with the
remaining reds exactly the receipt/suite byte bindings (H7 `digest=0,
header-lines=4, diff-clean=0`; H9 `valid=171` — the declared tail-sha no longer
matches the mutated bytes). That is the anti-tamper binding doing its job
against any byte mutation — not the patch. Patch attribution therefore uses the
**affected case's delta** (the wave-1 `MutKillList` detector), not the
letter-level tally; the letter-level rule ("selftest failure or closed<10/10")
is satisfied by every byte-mutated suite by construction, so it is recorded but
cannot discriminate.

## Patches (one find→replace per limb; all `bash -n` clean; scratch copies only)

| id | limb | find (exact bytes) | replace (exact bytes) | mutant sha256 | reopened class |
|---|---|---|---|---|---|
| M-H1 | H1 | `r40-closure\.sh` (inside the two `grep -qE '^\|[^|]*\`?r40-closure\.sh\`?[^|]*\|'` registry-row EREs, `check_h1` lines 569/571) | `r40-closure-renamed\.sh` (same two EREs) | `845176ba601d43c3bc1b3a4298ff3b6d8af86360f5a1febbb92ac045d033bdf5` | registry row for the suite not recognized (suite/registry-row pattern decoupled from the real artifact) |
| M-H2 | H2 | `if (index(s, "closed=7/8") > 0 && index(s, "failures=1") > 0) named++` (`h2_scan` line 594) | `named++` | `529b31ba29ec32afdb3799f2add7563d2b423bdb408fcb32a10b334e03097e6f` | correction line accepted without naming the final round-39 receipt values (`closed=7/8`, `failures=1`) |
| M-H3 | H3 | `'M39-2'` (both `check_h3` greps, lines 631/632) | `''` (empty -F pattern: counts every line / every table line) | `225d4f58671dc8b4f9027761ddaa3890f6cbc6e37397485d282d0522053e0841` | criterion row no longer required to cite M39-2 |
| M-H4 | H4 | `else if (c >= 1 && url && date && loc && c > w) { w = c; n = 1 }` (both quote loops, `h4_code` lines 662/670) | `else if (c >= 1 && url && loc && c > w) { w = c; n = 1 }` | `bd5dffa2e2c6d9d4a432ce4fff3a00bc50a9fb6c781e4e0f0db1c51d96ee6c05` | located quote accepted without an access date |
| M-H5 | H5 | `if [ -n "$rec" ] && [ -n "$want" ] && [ "$rec" = "$want" ]; then n=$((n + 1)); fi` (`payload_matches` line 428) | `if [ -n "$rec" ]; then n=$((n + 1)); fi` | `af761976a168aad61974e3a07c6738a680b5a7a6525679f206ac25e8205f6164` | recorded receipt payloads trusted on presence (the round-39 G2 forged-payload class) |

## Runs and verdicts

| mutant | selftest delta (patch-attributable) | plain run at Y (patch-attributable) | verdict |
|---|---|---|---|
| M-H1 | `case=H1 positive=fail mutants=3/3 verdict=fail`; positive payload `suite=1,digest=0,registry=0,registry-in=none` vs baseline `…digest=1,registry=1,registry-in=skill` — **registry=0 is the patch** (digest=0 is mode) | H1 red `registry=0` (+ mode `digest=0`); `closed=7/10 exit=1` (H5/H7 reds are the payload-match cascade) | **killed** |
| M-H2 | `case=H2 positive=pass mutants=2/3 verdict=fail` (3/3→2/3): `mutant=values-not-named rejected=0 rc=0 payload=corrections=4,named=4,missing=0,fences=closed` — the badvalues fixture is accepted; positive payload `named=8` vs baseline `named=5` | H2 payload `corrections=8,named=8` vs baseline `named=5` (limb still green); `closed=7/10 exit=1` (H1 mode red + H5/H7 cascade) | **killed** |
| M-H3 | `case=H3 positive=pass mutants=0/2 verdict=fail` (2/2→0/2): `row-absent-at-all rejected=0 rc=0 payload=mentions=5,rows=3` and `mention-without-criterion-row rejected=0 rc=0 payload=mentions=6,rows=2` — both fixtures accepted; positive payload `mentions=323,rows=83` vs baseline `mentions=1,rows=1` | H3 payload `mentions=323,rows=83` (limb still green); `closed=7/10 exit=1` (H1 mode red; H5 `forged-payload=accepted` + H7 red via the payload cascade — see observations) | **killed** |
| M-H4 | `case=H4 positive=pass mutants=3/3 verdict=pass` — **byte-identical to baseline**; no H4 detail line differs | H4 payload `s056=1,s058=1,s059=1,oversize=0` — **identical to baseline**; matched-bytes run at Y4: H4 green, payload identical, reds = H5/H7/H9 byte bindings only | **SURVIVED** |
| M-H5 | `case=H5 positive=fail mutants=1/2 verdict=fail` (2/2→1/2): `mutant=recorded-payload-contradicts-export rejected=0 rc=1 payload=…control=8/8…forged-payload=accepted…` (needle `control=7/8` miss) plus `positive=fail` and `control=canonical-source-green accepted=0` — three signals | **H5 red**: `control=8/8,forged-payload=accepted` vs baseline `control=8/8,forged-payload=rejected` — patch-attributable; `closed=7/10 exit=1` | **killed** |

In every mutant run the only OTHER case-line deltas vs baseline are the shared
mode signature (`case=H1 positive=fail`, `case=H5 positive=fail`,
`case=H7 positive=fail` with unchanged mutants counts) — present in all five,
caused by executing mutated bytes against the pristine export, excluded from
attribution (see the byte-self-binding block).

## H4 survivor (defect — selftest coverage gap on the quote/date conjuncts)

Dropping the `date` conjunct from `h4_code`'s two inhabit conditionals changes
**nothing observable**: `selftest_case_H4` is byte-identical to baseline
(`mutants=3/3`, all three fixtures still rejected) and the plain-run H4 payload
is identical. Reason: the three H4 fixtures are caught by the URL limb
(`nourl` → `url=0`) and the 25-word cap branch (`oversize` → `c>25` → `over++`
before the else-if), so no fixture isolates the quote-presence or date
conjuncts; any condition-line weakening of `quote`/`date` survives.

The conjunct IS load-bearing in the committed check — direct probe
(`check_h4` sourced from each suite copy, same fixture tree):

- fixture: a round-39 Gate block for S056 with URL + located quote + location
  token but **no access date** (delivered byte-exact as
  `.ufo/waves/round-40/wave2/MutH1H5.h4-nodate.txt`, 723 bytes, sha256
  `c362572072d465fd9c0ec807dcaf4e33004ac3648f5a9351480c19a9dc5bc00a`);
- pristine `bdbd18a3…`: rc=1, `payload=s056=0,s058=1,s059=1,oversize=0` (red —
  the date requirement fires);
- mutant `bd5dffa2…`: rc=0, `payload=s056=1,s058=1,s059=1,oversize=0` (green —
  the class is reopened).

So the committed check would red a date-less block on the real lane, but the
suite's own graded selftest cannot detect a check mutated to stop requiring it.
**Fix (L1's call):** add a date-less-block fixture to `selftest_case_H4` (e.g.
`cases=quote-date-absent`: url + location + ≤25-word quote, no access date;
needle the `s056=0` red), and ideally a quote-less counterpart for the
quote-presence conjunct. No C1 kill-rule breach by the committed bytes: the
committed suite rejects the probe fixture (pristine rc=1 above).

## Observations (recorded; L1's call, no contract change)

1. **H5's forged detection is relative.** `forged=rejected` requires
   `payload_matches(forged) < control`; when another payload is already
   mismatched (cascade state), replacing that same line no longer lowers the
   count — mutH3's plain run shows `forged-payload=accepted` caused by the
   patch-caused H3 payload delta (`mentions=323,rows=83`). The run is already
   red in that state through H5's control gate and H7's cmp, so this is
   defense-in-depth layering, not a standalone hole.
2. **The M-H5 patch also blinds H7's `payload-match` value comparison.**
   `payload_matches` is shared: under the trust patch it degrades to
   presence-counting (mutH5's plain run prints `payload-match=9` while two
   payload values contradict the receipt). H7's `cmp` limb still reds the run
   (byte identity), but no graded H7 fixture isolates either the value
   comparison or `cmp` — consistent with wave-1 MutKillList M11 (cmp ungraded)
   and M08 (forged fixture tampers only the H3 id). Family fix: one fixture
   with a wrong-but-well-formed non-H7 payload value, and one shape-clean
   byte-different (reordered) receipt.

## Restoration and hygiene

- Pristine re-runs after ALL mutant runs: plain at Y **byte-identical** to the
  baseline transcript (rc=0, `closed=10/10 exit=0`); selftest at Y
  **byte-identical modulo the `--work` path** embedded in the H6
  unreadable-root fixture's stderr line (sed-normalized `cmp` clean) — rc=0,
  `cases=10 failures=0`.
- Mutants were separate scratch copies; the extracted pristine bytes re-hashed
  `bdbd18a3…` after all runs; the lane's committed suite re-hashed from
  `git show HEAD:corpus/instruments/r40-closure.sh` = `bdbd18a3…` (unchanged).
- Lane working tree at yield: untracked `.ufo/waves/round-40/final-gates/`,
  `kasegi-r40-falsify.ready{,.dispatched}`, `wave2/` only — the same set as at
  seat start plus this seat's two wave2 deliverables; zero tracked-file
  modifications; no mutating git/jj command anywhere (the only commits are the
  two fixture commits inside the seat clone, toplevel-asserted).
- Scratch S removed before this receipt was finalized; no `kasegi-r39*`/
  `kasegi-r40*` entry survives from this seat under the real scratch root (all
  suite runs used `--scratch-root` inside S).

## Verdict

**4 killed (H1, H2, H3, H5), 1 survived (H4). The survivor is a defect: the
graded selftest does not pin H4's quote/date conjuncts** (fixture-set gap;
probe-delivered). C1's two counting commands reproduce green at the Y fixture
(byte-identical tee + clean graded selftest), so the frozen C1 predicate stands
as measured; the H4 finding is a selftest-coverage improvement for the suite,
not a false claim.

Report: `.ufo/waves/round-40/wave2/MutH1H5.md` (this file). Fixture:
`.ufo/waves/round-40/wave2/MutH1H5.h4-nodate.txt`.
