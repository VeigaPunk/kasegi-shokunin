# R46bRevClaimsErrata — counter lineage audit across attempts 1 and 2

VERDICT: HOLDS

Seat scope: (1) audit the counter lineage v1 → v1.1 → v1.2 and diff the frozen counters at
`eb874bc86ad7a6cfec299088e5a2d7ec68cf61b7` against the live files; (2) enumerate every
claim-sentence in the attempt-1 claims file whose verification status the attempt-2 work
changes; (3) name the errata entries the attempt-2 report must carry. Read-only audit; no
fixtures built, no scratch created, no git mutation performed. All commands run 2026-10-29
against lane repo `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (HEAD `ee03806b6b54a2822045e96641a77fa76984b410`).

## Finding 1 — Lineage intact, zero drift (the assigned check)

Command (exactly as assigned):

```
git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin diff eb874bc HEAD -- corpus/instruments/r46-c1-gate.py corpus/instruments/r46-c2-gate.py
```

Output: **(empty), exit 0** — both counters byte-identical from the attempt-1 integration tip
(`eb874bc`, "round-46: QUALITY R50-R52, counter errata E2, final-measure script, wave-2
reports", 2026-10-28 21:42:56 -0300) to HEAD. No drift; the attempt-2 freeze leaves both
untouched, as the freeze record itself claims:

> `.ufo/waves/round-46/attempt2/freeze.txt`: "the attempt-1 instruments r46-c1-gate.py /
> r46-c2-gate.py and their selftests are byte-identical to base 04af9bc9 at this freeze
> (verified: git diff base..HEAD empty on those paths at freeze time); the round's C1 work
> extends the selftests and the battery only"

My independent re-verification of that freeze note:

```
git diff --stat 04af9bc9..HEAD -- corpus/instruments/r46-c1-gate.py corpus/instruments/r46-c2-gate.py \
  corpus/instruments/r46-counters-selftest-c1.py corpus/instruments/r46-counters-selftest-c2.py
→ (empty), exit 0
```

Version-chain hashes (each computed with `git show <rev>:<path> | sha256sum`):

| version | commit | r46-c1-gate.py | r46-c2-gate.py |
|---|---|---|---|
| v1 (attempt-1 freeze) | `9f23aab` | `b0c730c834b4d7c6b16ac56f8c574ac599e8ae651aa02c5b2408fd736dd82294` | `0ee958578b5923706178081a94dae471682f02f74492bb4a3b54a118c12ec3f6` |
| v1.1 (E1 commit) | `5437afe` | `99e0ee555b68e5177f33e49e8024469608297a412171b190f66b1bba189475cc` | `b52fea3183a393fa2f5bb40879241034e9db0b45f7914244d9f3bed134958621` |
| v1.2 (wave-2 fixes) | `93140c1` | `95f2eb7933841d6cd06a0041af613204cbfe29e96a38a218499a71846cdb03b7` | `647bd5b7b62685519d8d396bf2d02eca7ad0bb440dd5c4041beabfaa45ea2909` |
| live | `HEAD` = `ee03806` | `95f2eb7933841d6cd06a0041af613204cbfe29e96a38a218499a71846cdb03b7` | `647bd5b7b62685519d8d396bf2d02eca7ad0bb440dd5c4041beabfaa45ea2909` |

The v1 hashes match `.ufo/waves/round-46/freeze.txt` exactly; the v1.1 hashes match the
"at the integration tip" values recorded in `.ufo/waves/round-46/counter-errata.md` E1
section exactly (c1 `99e0ee…` is the counter at `5437afe`, the commit that itself landed the
E1 errata — `git diff --stat 8e927e9 5437afe -- corpus/instruments/r46-c1-gate.py` prints
`1 file changed, 25 insertions(+), 2 deletions(-)`, the allow-list hardening; this is version
progression inside attempt 1, not drift). File history: `git log --oneline --follow` shows
the last mutation of both counters at `93140c1` for each. The errata file's hash records are
accurate; the lineage story in `counter-errata.md` is internally consistent.

Do-nothing control for this check: the null hypothesis is "counters drifted after the lineage
tip." The empty diff (plus the independent `04af9bc9..HEAD` empty diff, plus hash equality at
every link) discriminates against it. A do-nothing tree changes nothing here because there is
nothing to change — the check is pure read-only comparison.

## Finding 2 — Attempt-1 claim-sentences whose verification status attempt-2 changes

Attempt-1 claims (`.ufo/waves/round-46/claims.json`, frozen `9f23aab`, sha256
`e56ebf872b6073964d98812608275f5799afc9ee2334d4aab1363c06e59cd740`) "landed their work but
were never adjudicated" (attempt-2 `claims.json` note field). The attempt-2 work touches the
same frozen counters only through their selftests and the battery
(`.ufo/waves/round-46/attempt2/controls/selftest-baselines.txt`, run 2026-10-29 at base
`04af9bc9`, re-ran both harnesses: `selftest cases=76 failures=0` / `selftest cases=137
failures=0`). Enumerated status changes:

1. **C1 `expect_after` "c1-gate fixed=7/7 exit=0" — STRENGTHENED, condition unchanged.**
   The reading recorded at the attempt-1 tip (`.ufo/waves/round-46/controls/final-measure.txt:21`
   `c1-gate fixed=7/7 exit=0`) is re-graded on a larger falsification surface: the extended
   selftests (target `cases>76 failures=0`) plus the battery's 20 c1 mutants, all required
   caught-or-equivalent with committed proofs (`uncaught=0`; frozen before-value
   `mutbat counter=c1 mutants=20 caught=13 equivalent=0 uncaught=7 baseline_failures=0` per
   `.ufo/waves/round-46/attempt2/controls/mutbat-before.txt`). No counter text changed, so
   the sentence's truth condition is identical; its epistemic status moves from
   "76-case selftest-graded, measured once" to "mutation-covered".

2. **C1 `after` (counter-graded portion) — same strengthening; semantic portion unchanged.**
   The re-grounding outcome for the pair (claim-package-contract.md, claim-gates.md) is
   re-derived by the same mechanism as (1). The sentence's non-author semantic clause ("a
   non-author reading finds a re-grounded entry whose rows do not support the entry's current
   claims") is NOT re-exercised by attempt-2 — no attempt-2 seat re-reads the two entries'
   rows; that status stays as attempt-1 wave-2 left it.

3. **C2 `expect_after` "c2-gate fixed=7/7 exit=0" — STRENGTHENED on grading, VOIDED on
   reproducibility. Dual status change; this is the load-bearing cross-attempt finding.**
   (a) Grading axis: same strengthening as (1) via the 21 c2 mutants (before-value
   `mutbat counter=c2 mutants=21 caught=8 equivalent=0 uncaught=13 baseline_failures=0`).
   (b) Reproducibility axis: the frozen c2-gate is hard-pinned to attempt-1's target state —
   `corpus/instruments/r46-c2-gate.py:179` `if len(rows) != 28 or adm != 28 or dup:` (G1) and
   `:347` `return (len(names) == 65 and len(everything) == 65 and nested == 65 and base_ok
   and sized), …` (G6; docstring lines 10 and 32-35 say "exactly 28 rows" and "`… wc -l`
   == 65"). Attempt-2's C2 admits F29: `claims.json` `after` says "29 admitted frontier rows …
   one new knowledge entry (66 total)". On any post-F29 tree, frozen G1 and G6 both fail, so
   the frozen counter cannot print 7/7 there regardless of the F29 content's quality. The
   attempt-1 sentence thereby stops being reproducible on the successor tree under the frozen
   counter. The attempt-2 claims anticipate the conflict: `claims.json` `frontier_step` says
   "… lands this round together with the r46-c2-gate.py ledger-exemption amendment if the
   wave verifies it, else the deferral is carried". As of HEAD `ee03806` the live tree still
   holds 65 entries / 28 rows / 73 SOURCES rows (F29 not yet integrated), and **no amendment
   exists** — the counter is byte-identical (Finding 1) and `grep -n "ledger\|considerthese"
   corpus/instruments/r46-c2-gate.py` prints nothing (exit 0, empty).

4. **C2 `after` — same dual change.** Its sub-sentence "one new knowledge entry (65 total)"
   is superseded by the 66-entry post-F29 tree; the S073-sha, quote-location and
   frozen-cores sub-sentences are unaffected by attempt-2 (S073 and its manifest stay pinned;
   the attempt-2 claims pin the attempt-1 manifest sha256 `01f02572…` byte-identical).

5. **C2 `kill_rule` tail "The target (28 admitted rows, 65 entries) is not narrowed after
   landing." — SUPERSEDED, not falsified.** Growth is not narrowing, but the pinned numbers
   go stale the moment F29 lands; the standing not-to-be-narrowed target becomes 29 rows / 66
   entries (attempt-2 C2 `kill_rule`). Verification status: moot as a guard over the current
   tree.

6. **C1 `kill_rule` errata clause and C2's counter-integrity expectation — UNCHANGED,
   still satisfied.** No limb sentence of either counter changed after attempt-1 scoring
   (byte-identical through HEAD), so attempt-2 triggers no new counter erratum. The clause's
   standing log remains `.ufo/waves/round-46/counter-errata.md` (E1, E2). Note the attempt-2
   C1 `kill_rule` repeats the same clause with "logged as errata in **the attempt-2 errata
   file**" — a new E3 is only owed if a counter amendment actually lands (see Finding 3).

7. **Unchanged-status set (explicitly enumerated to close the space):** C1 `before`
   (executes=40 gated=24 broken=0; 23 `test -d ~/Projects/…` lines), C1 `expect_before`
   (1/7), C1 `freeze_tree_reading` (1/7 at `9f23aab`), C2 `before` (27 rows / 64 entries /
   72 SOURCES; sweep prints nothing; base 1/7, freeze 2/7), C2 `expect_before` (1/7), C2
   `freeze_tree_reading` (2/7), both `plain[]` arrays, `sourced_claim` (S073), and
   `frontier_step` — all are frozen historical readings at `914ca0b` / `9f23aab`; attempt-2
   neither re-runs the old counters against the old base for adjudication nor edits any
   before-value. The attempt-2 do-nothing-control requirement re-derives attempt-2's own
   before-values, not attempt-1's; these sentences keep their frozen status "stated,
   unadjudicated".

Corollary checked (c1 side): the frozen c1-gate's `TARGET_GATED = 22`
(`corpus/instruments/r46-c1-gate.py:58`) is a hard pin, but the F29 entry's recheck line
(source-recheck over committed S074 bytes) classifies as `executes` on a tree that holds
those bytes — `corpus/instruments/recheck-audit.py:160-162`
`"class": "executes" if lane_rc == 0 else ("gated" if limbs["parse"] else "broken")` — so it
does not move the gated count off 22, and L2 is computed against the `--baseline` export
(gated(BASE)=24, R=the re-grounded pair). Frozen c1-gate is therefore *structurally capable*
of still reading 7/7 on the post-F29 tree; unlike c2-gate there is no hard count pin. This
is mechanism analysis, not a re-run — see Limitations.

## Finding 3 — Errata entries the attempt-2 report must carry

1. **E1 (v1 → v1.1), in full** — C1-E1…E6, C2-E1…C2-E6, both "forced by" columns, and the
   "Not changed on purpose" disclosure (environment not scrubbed of `HOME`; the L2 host-
   dependence rationale). The frozen counters' docstrings name "errata E1 and E2, see
   .ufo/waves/round-46/counter-errata.md"; any attempt-2 quotation of a c1/c2-gate verdict
   inherits this log.
2. **E2 (v1.1 → v1.2), in full** — C1-E7…E10, C2-E7…C2-E12, the landing-gate
   `date-order-author` withdrawal (selftest now asserts the round-45 honest-rewrite shape
   passes), and **the critic's-objection disclosure with its five answers** — in particular
   answer 1 ("the sentence made literal" withdrawn for C1 L4/L6/L7, the token floor and every
   C2 change: they are new requirements) and answer 4 (the v1.2 pass-set is wider on the
   exempt-entry axis, narrower on every other). A reader weighing the attempt-1 C1 kill-rule
   parenthesis narrowly must read C1 as UNVERIFIED on the frozen counter and rely on the
   plain re-derivations — the attempt-2 report must carry that pointer too.
3. **E3 — CONDITIONAL, NEW, and currently absent.** If the wave lands the contemplated
   `r46-c2-gate.py` amendment (the "ledger-exemption" of attempt-2 `claims.json`
   `frontier_step`, required because frozen G1 pins 28 rows and G6 pins 65 entries while the
   F29 admission makes 29/66 — Finding 2 item 3), it MUST be logged as a new erratum in the
   attempt-2 errata file with a plain re-derivation that does not use the counter, per both
   the attempt-1 C1 kill-rule parenthesis and the attempt-2 C1 kill rule's errata clause.
   Verified absent as of HEAD `ee03806`: counters byte-identical (Finding 1), no
   `.ufo/waves/round-46/attempt2/counter-errata.md` exists. **If the amendment does not
   land, the attempt-2 report must instead record the deferral and must not quote any frozen
   c2-gate reading on the post-F29 tree** — under the frozen counter no such reading can be
   7/7, and claiming one would falsify the attempt-2 claims' own freeze note ("the attempt-1
   counters … are NOT edited by this round's claims (any amendment is a logged erratum)").

## Limitations

- I did not re-run the battery or the extended selftests (owned by other seats); "STRENGTHENED"
  in Finding 2 rests on the frozen receipts (`controls/selftest-baselines.txt` 76/0 and 137/0 at
  base `04af9bc9`; `controls/mutbat-before.txt` uncaught 7/13) plus the attempt-2 claims' own
  after-conditions, which were **not yet re-run at HEAD** — the wave is in flight and no
  after-receipt exists yet. If the wave fails to reach `uncaught=0`, items 1-3 of Finding 2
  downgrade from strengthened to unproven.
- The "ledger-exemption amendment" text is unspecified anywhere I can read; I verified only
  its absence at HEAD, not its eventual content. If it lands, it must be reviewed against
  Finding 3 item 3.
- The c1-gate 7/7-on-F29-tree claim in Finding 2's corollary is mechanism analysis from the
  committed code (`TARGET_GATED = 22`, recheck-audit classification), not a re-run; the L1
  final measure should re-run the frozen c1-gate (`--root <post-F29 tree> --baseline
  <914ca0b export>`) to close it.
- Attempt-1's own adjudication (were its claims true at its tip?) remains out of scope for
  attempt-2; this audit covers only which of its sentences change status under attempt-2's work.
- No scratch directory was created (no fixtures); nothing to remove. No files were modified
  except this Report.
