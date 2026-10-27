# ScoutReceiptShape — round-41 receipt format spec (I2 target)

Seat: ScoutReceiptShape (leaf scout, no subagents). Lane repo read-only except
this receipt + deliverable; scratch at /fast/scratch/hyaku/kasegi-r41/ScoutReceiptShape
(removed at yield). No tool installs, no network fetches, no git/jj mutations.

Deliverable: `.ufo/waves/round-41/wave1/ScoutReceiptShape.txt`
- 210 lines, sha256 `9b7785a6f6544839486da04739440b595016a0ac1939710fb4aea2d0aa743930`
- Contains ONLY the format spec (line layout + derivation commands + identity
  checks + production/negative-control semantics). Validation evidence is here.

## Sources studied (all lane reads, absolute paths)

1. `.ufo/waves/round-41/claims.json` (frozen claims, read first) — C1 predicate:
   receipt at Y = "teed transcript of BOTH the suite run and the graded selftest";
   kill rule: "the receipt at Y not byte-identical to the teed transcript of the
   run that produced it" reds the claim. I2 names `time-basis=ref-commit`,
   run-utc = ref committer instant.
2. `.ufo/waves/round-40/final-gates/all-gates.txt` — the r40 receipt, 16 lines:
   `all-gates v4` + `export-ref=c7aea5e…` (J7, NOT the Y commit d0fe34d) +
   `suite-sha256=bdbd18a3…` + `time-basis=ref-commit` + `run-utc=2026-10-26T22:32:37Z`
   + 10 `H<n> payload=… closed=1` lines + `closed=10/10 exit=0`.
3. `corpus/instruments/r40-closure.sh` (1734 lines) — the receipt machinery:
   - contract block lines 93–138 (v4: transcript not summary; run-utc =
     `git log -1 --format=%ct` rendered UTC, NOT wall clock — the r39 R1/M39-1
     false-provenance defect was a wall-clock stamp outrunning its commit).
   - `ref_utc()` lines 371–377: `git -C "$LANE" log -1 --format=%ct $1` →
     `TZ=UTC date -u -d "@$e" +%Y-%m-%dT%H:%M:%SZ`.
   - `receipt_shape()` lines 440–482: sentinel/ref/digest/time-basis/run-utc/
     not-future/header-lines/run-lines/body-lines/closed-0/closed-line.
   - `assemble_transcript()` lines 489–512: `export-ref` adopts the committed
     receipt's declared ref when present, else the run's own ref.
   - `check_h7()` lines ~799–850: rebuilds canonical transcript, `cmp -s` vs
     committed file; ancestor (`merge-base --is-ancestor`) + diff-clean
     (`diff --name-only` = receipt path only) limbs.
   - `run_suite_report()` lines ~988–1046: `--receipt-out` seeds a pending
     receipt, iterates the transcript to fixpoint (≤4), prints transcript to
     stdout; a red run's receipt carries its own red flags — "a receipt is
     never a tally the run did not print".
   - `run_selftest()` lines 1605–1698: `selftest case=H<i> positive=…
     mutants=<ok>/<n> verdict=…` + detail/judge lines + `selftest cases=10
     failures=<k>`; `judge_selftest_report()` lines 1577–1603 rejects forged
     summaries (case-count, verdict, mutants=0/0, detail cross-check).
4. `corpus/lessons/round-40-verifier-spotcheck.md` §5: D2 = "Y-level selftest
   tally quoted without a transcript (violates the lane's own R37)… The receipt
   has no selftest line". §1 confirmed `git diff --name-only J7 Y` =
   `.ufo/waves/round-40/final-gates/all-gates.txt` only.
5. Sibling `wave1/CritReceiptUtc.md` — independently verified the run-utc
   derivation binds to the receipt's NAMED export-ref (J7 → 22:32:37Z, not
   Y's 22:33:07Z), `%ct` epoch is timezone-immune, `%cI` text is not (keeps
   `-03:00`). My spec matches its findings; no conflict.

## Commands actually run (evidence)

```
$ git -C lane log -1 --format='%H %ct %cI' c7aea5ef97902f38289cbdc1cf267068876a62dd
c7aea5ef… 1793053957 2026-10-26T19:32:37-03:00
$ TZ=UTC date -u -d @1793053957 +%Y-%m-%dT%H:%M:%SZ
2026-10-26T22:32:37Z          # == committed receipt run-utc, byte-exact
$ git -C lane diff --name-only c7aea5e d0fe34d
.ufo/waves/round-40/final-gates/all-gates.txt   # receipt-only J→Y diff
$ sha256sum + wc -l on committed r40 receipt → 16 lines
$ ls corpus/instruments → only r40-closure.sh; r41 suite not yet landed
```

## Format decisions (what the spec fixes and why)

- **31-line layout, order locked**: 5 header lines (sentinel `all-gates v1`,
  export-ref, suite-sha256, time-basis=ref-commit, run-utc) → 12 `I<n>
  payload=… closed=<0|1>` run lines → 12 `selftest case=I<n> …` graded lines →
  `selftest cases=12 failures=0` → `closed=12/12 exit=0` as the FINAL line.
  The seat spec enumerates the components in exactly this order with the
  closed line last; this also makes the receipt a single coherent tee whose
  final tally covers both the run and the embedded graded selftest (the D2
  fix: the selftest transcript is now INSIDE the committed receipt, not a
  scratch-only tally).
- **`export-ref` names J, not Y** (parent commit; a commit cannot contain its
  own hash). At Y the transcript adopts the committed receipt's declared ref
  (r40 `assemble_transcript` rule) so a re-run at Y re-prints the J-produced
  bytes.
- **run-utc = `ref_utc(export-ref)`**: `git log -1 --format=%ct <ref>` →
  `TZ=UTC date -u -d "@$e" +%Y-%m-%dT%H:%M:%SZ`. Verified byte-exact against
  the committed r40 receipt (1793053957 → 2026-10-26T22:32:37Z).
- **Byte-identity** both ways: verifier-side `cmp -s` of a canonical rebuild
  (self-reference closed by rebuilding the I2 line from the receipt minus its
  own line, r40 h7_inner pattern; payload-match per non-I2 id; selftest block
  re-graded) + operator-side re-run-with-tee then `diff`/`cmp -s` empty.
- **Selftest block = 12 case lines + summary only**; all detail/judge/
  `selftest export-ref=` diagnostics must go to stderr so the receipt tees a
  verbatim 13-line graded transcript. Case line keeps r40's graded shape
  `positive=… <evidence incl. mutants=<ok>/<n>, n≥1> verdict=<pass|fail>` as
  the recommended grammar — the I9 per-case payload-comparison fact rides in
  the middle fields.
- **Green window**: at J the absent receipt reds I2 → `closed=11/12 exit=1`;
  produce via `--receipt-out` at J (seeded pending receipt so the written
  bytes already carry the green I2 verdict + green selftest block), commit
  those exact bytes only when they read `closed=12/12`, Y = J + receipt-only
  diff.

## Remaining unknowns / boundaries

- Exact interior payload keys and selftest evidence fields are the suite
  author's choice; the spec pins line grammar, counts, order and required
  tokens only. If the r41 suite interleaves `selftest detail=`/`judge=` lines
  on stdout, they must be redirected to stderr (or the receipt block becomes a
  projection — less clean; spec recommends stderr).
- Host-sensitive I6 scratch scan: produce/verify on a scratch root with zero
  `kasegi-r41*` strays other than the run's --work (documented limit, carried
  from r40 H6).
- r41 suite file not yet present in lane (only r40-closure.sh); spec written
  against frozen claims + r40 machinery + peer CritReceiptUtc findings.
